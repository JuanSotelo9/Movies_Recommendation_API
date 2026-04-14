"""
Ejecuta las 3 consultas benchmark y muestra los resultados
en consola Y en una ventana gráfica con tkinter.
"""

import tkinter as tk
from tkinter import ttk, font
import threading

from db.postgres import init_pool, close_pool
from db.neo4j    import init_driver, close_driver
from services.benchmark import (
    query_friends_movies,
    query_actor_network,
    query_genre_suggestions,
)

# ── Parámetros de las consultas ──────────────────────────────
USER_ID      = 1   # Carlos Mendoza
ACTOR_ID     = 1   # Leonardo DiCaprio
MOVIE_ID     = 1   # Inception (referencia para Q3)
MIN_RATING   = 4.0
TOLERANCE    = 0.5

# ── Colores ──────────────────────────────────────────────────
C_BG         = "#0f1117"
C_PANEL      = "#1a1d27"
C_BORDER     = "#2a2d3a"
C_NEO4J      = "#00c4a0"   
C_POSTGRES   = "#4f8ef7"   
C_WIN        = "#f5c542"   
C_TEXT       = "#e8eaf0"
C_MUTED      = "#6b7280"
C_Q1         = "#7c6af7"
C_Q2         = "#f76a6a"
C_Q3         = "#f7a26a"


# ══════════════════════════════════════════════════════════════
#  CONSOLA — impresión de resultados
# ══════════════════════════════════════════════════════════════

def sep(titulo: str, ancho: int = 60):
    print(f"\n{'═' * ancho}")
    print(f"  {titulo}")
    print(f"{'═' * ancho}")

def barra_tiempo(ms: float, max_ms: float, largo: int = 30) -> str:
    proporcion = ms / max_ms if max_ms > 0 else 0
    lleno = int(proporcion * largo)
    return "█" * lleno + "░" * (largo - lleno)

def imprimir_benchmark(label_neo: str, ms_neo: float, label_pg: str, ms_pg: float):
    max_ms = max(ms_neo, ms_pg)
    ganador = "Neo4J" if ms_neo < ms_pg else "PostgreSQL"
    diferencia = abs(ms_neo - ms_pg)
    pct = (diferencia / max_ms * 100) if max_ms > 0 else 0

    print(f"\n  ⏱  TIEMPOS DE EJECUCIÓN")
    print(f"  {'Neo4J':<12} {ms_neo:>8.2f} ms  {barra_tiempo(ms_neo, max_ms)}")
    print(f"  {'PostgreSQL':<12} {ms_pg:>8.2f} ms  {barra_tiempo(ms_pg, max_ms)}")
    print(f"\n  🏆 Ganador: {ganador}  ({pct:.1f}% más rápido)")

def imprimir_q1(r):
    sep(f"CONSULTA 1 — Películas de amigos no vistas  (user_id={r.user_id})")
    print(f"  Películas encontradas: {len(r.results)}\n")
    for i, m in enumerate(r.results, 1):
        amigos = ", ".join(f"{f['name']} ({f['rating']}★)" for f in m.friends_who_watched)
        print(f"  {i}. {m.title} ({m.year})  —  prom. amigos: {m.avg_friend_rating}★")
        print(f"     Visto por: {amigos}")
    imprimir_benchmark("Neo4J", r.benchmark.neo4j_ms, "PostgreSQL", r.benchmark.postgres_ms)

def imprimir_q2(r):
    actor_x_name = r.actor_x['name'] if isinstance(r.actor_x, dict) else getattr(r.actor_x, 'name', '?')
    sep(f"CONSULTA 2 — Red de actores  (actor_x={actor_x_name})")
    print(f"  Actores a 2 grados de separación: {r.total_found}\n")
    for i, a in enumerate(r.results[:8], 1):
        path = a.connection_path
        if path:
            item = path[0]
            actor = item['actor'] if isinstance(item, dict) else getattr(item, 'actor', '?')
            movie = item['movie'] if isinstance(item, dict) else getattr(item, 'movie', '?')
            puente = f"vía {actor} en '{movie}'"
        else:
            puente = ""
        print(f"  {i}. {a.name}  {puente}")
    if r.total_found > 8:
        print(f"     ... y {r.total_found - 8} más")
    imprimir_benchmark("Neo4J", r.benchmark.neo4j_ms, "PostgreSQL", r.benchmark.postgres_ms)

def imprimir_q3(r):
    sep(f"CONSULTA 3 — Géneros sugeridos  (user_id={USER_ID}, ref='{r.reference_movie['title']}')")
    print(f"  Mis géneros favoritos: {', '.join(r.my_genres)}")
    print(f"  Mi calificación de {r.reference_movie['title']}: {r.reference_movie['my_rating']}★\n")
    print(f"  Géneros sugeridos:")
    for g in r.suggested_genres:
        barra = "▓" * int(g.score * 20)
        ejemplos = ", ".join(m["title"] for m in g.sample_movies[:2])
        print(f"  • {g.genre:<14} score={g.score:.2f}  {barra}")
        if ejemplos:
            print(f"    Ej: {ejemplos}")
    imprimir_benchmark("Neo4J", r.benchmark.neo4j_ms, "PostgreSQL", r.benchmark.postgres_ms)


# ══════════════════════════════════════════════════════════════
#  VENTANA GRÁFICA
# ══════════════════════════════════════════════════════════════

class BenchmarkApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Neo4J vs PostgreSQL — Benchmark")
        self.root.configure(bg=C_BG)
        self.root.geometry("960x780")
        self.root.resizable(True, True)
        self._build_ui()

    # ── Construcción de la UI ─────────────────────────────────

    def _build_ui(self):
        # Encabezado
        hdr = tk.Frame(self.root, bg=C_BG)
        hdr.pack(fill="x", padx=24, pady=(20, 0))

        tk.Label(hdr, text="Neo4J  vs  PostgreSQL",
                 bg=C_BG, fg=C_TEXT,
                 font=("Helvetica", 20, "bold")).pack(side="left")

        self.btn = tk.Button(
            hdr, text="▶  Ejecutar benchmarks",
            command=self._run_async,
            bg=C_NEO4J, fg=C_BG, relief="flat",
            font=("Helvetica", 12, "bold"),
            padx=18, pady=6, cursor="hand2",
        )
        self.btn.pack(side="right")

        self.status = tk.Label(hdr, text="Listo", bg=C_BG, fg=C_MUTED,
                               font=("Helvetica", 11))
        self.status.pack(side="right", padx=16)

        # Notebook con tabs por consulta
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Dark.TNotebook",       background=C_BG,    borderwidth=0)
        style.configure("Dark.TNotebook.Tab",   background=C_PANEL, foreground=C_MUTED,
                        padding=[16, 8],        font=("Helvetica", 11))
        style.map("Dark.TNotebook.Tab",
                  background=[("selected", C_BORDER)],
                  foreground=[("selected", C_TEXT)])

        self.nb = ttk.Notebook(self.root, style="Dark.TNotebook")
        self.nb.pack(fill="both", expand=True, padx=24, pady=16)

        self.tabs = {}
        for label, color in [
            ("Q1 — Películas de amigos", C_Q1),
            ("Q2 — Red de actores",      C_Q2),
            ("Q3 — Géneros sugeridos",   C_Q3),
        ]:
            frame = tk.Frame(self.nb, bg=C_PANEL)
            self.nb.add(frame, text=label)
            self.tabs[label] = frame

        self._build_q1_tab(self.tabs["Q1 — Películas de amigos"])
        self._build_q2_tab(self.tabs["Q2 — Red de actores"])
        self._build_q3_tab(self.tabs["Q3 — Géneros sugeridos"])

    # ── Widgets compartidos ───────────────────────────────────

    def _panel(self, parent, title: str, color: str) -> tk.Frame:
        outer = tk.Frame(parent, bg=color, bd=0)
        outer.pack(fill="x", padx=20, pady=(16, 0))
        inner = tk.Frame(outer, bg=C_PANEL, bd=0)
        inner.pack(fill="x", padx=2, pady=(0, 2))
        tk.Label(inner, text=title, bg=C_PANEL, fg=color,
                 font=("Helvetica", 12, "bold"),
                 anchor="w", padx=14, pady=8).pack(fill="x")
        body = tk.Frame(inner, bg=C_PANEL)
        body.pack(fill="x", padx=14, pady=(0, 12))
        return body

    def _benchmark_bar(self, parent, color: str):
        """Crea el widget de barra comparativa de tiempos."""
        frame = tk.Frame(parent, bg=C_PANEL)
        frame.pack(fill="x", padx=20, pady=(12, 20))

        tk.Frame(frame, bg=C_BORDER, height=1).pack(fill="x", pady=(0, 12))
        tk.Label(frame, text="⏱  Tiempo de ejecución",
                 bg=C_PANEL, fg=C_MUTED,
                 font=("Helvetica", 10)).pack(anchor="w")

        row_neo = tk.Frame(frame, bg=C_PANEL)
        row_neo.pack(fill="x", pady=3)
        tk.Label(row_neo, text="Neo4J     ", bg=C_PANEL, fg=C_NEO4J,
                 font=("Helvetica", 11, "bold"), width=12, anchor="w").pack(side="left")
        bar_neo = tk.Canvas(row_neo, bg=C_BG, height=18,
                            highlightthickness=0, width=400)
        bar_neo.pack(side="left", padx=(0, 8))
        lbl_neo = tk.Label(row_neo, text="— ms", bg=C_PANEL, fg=C_NEO4J,
                            font=("Helvetica", 11), width=10, anchor="w")
        lbl_neo.pack(side="left")

        row_pg = tk.Frame(frame, bg=C_PANEL)
        row_pg.pack(fill="x", pady=3)
        tk.Label(row_pg, text="PostgreSQL", bg=C_PANEL, fg=C_POSTGRES,
                 font=("Helvetica", 11, "bold"), width=12, anchor="w").pack(side="left")
        bar_pg = tk.Canvas(row_pg, bg=C_BG, height=18,
                           highlightthickness=0, width=400)
        bar_pg.pack(side="left", padx=(0, 8))
        lbl_pg = tk.Label(row_pg, text="— ms", bg=C_PANEL, fg=C_POSTGRES,
                          font=("Helvetica", 11), width=10, anchor="w")
        lbl_pg.pack(side="left")

        lbl_winner = tk.Label(frame, text="", bg=C_PANEL, fg=C_WIN,
                               font=("Helvetica", 12, "bold"))
        lbl_winner.pack(anchor="w", pady=(8, 0))

        return {
            "bar_neo": bar_neo,
            "bar_pg": bar_pg,
            "lbl_neo": lbl_neo,
            "lbl_pg": lbl_pg,
            "lbl_winner": lbl_winner,
        }

    def _update_bars(self, widgets: dict, neo_ms: float, pg_ms: float):
        MAX_W = 400
        max_ms = max(neo_ms, pg_ms, 0.01)

        w_neo = int((neo_ms / max_ms) * MAX_W)
        w_pg  = int((pg_ms  / max_ms) * MAX_W)

        for canvas, w, color in [
            (widgets["bar_neo"], w_neo, C_NEO4J),
            (widgets["bar_pg"],  w_pg,  C_POSTGRES),
        ]:
            canvas.delete("all")
            canvas.create_rectangle(0, 0, MAX_W, 18, fill=C_BG,    outline="")
            canvas.create_rectangle(0, 0, w,     18, fill=color,   outline="")

        widgets["lbl_neo"].config(text=f"{neo_ms:.2f} ms")
        widgets["lbl_pg"].config(text=f"{pg_ms:.2f} ms")

        if neo_ms < pg_ms:
            pct = (pg_ms - neo_ms) / pg_ms * 100
            widgets["lbl_winner"].config(text=f"🏆 Neo4J fue {pct:.1f}% más rápido")
        else:
            pct = (neo_ms - pg_ms) / neo_ms * 100
            widgets["lbl_winner"].config(text=f"🏆 PostgreSQL fue {pct:.1f}% más rápido")

    # ── Tab Q1 ────────────────────────────────────────────────

    def _build_q1_tab(self, parent):
        desc = tk.Label(
            parent,
            text=f"Películas que los amigos de Carlos (user {USER_ID}) calificaron >{MIN_RATING}★ y él aún no ha visto",
            bg=C_PANEL, fg=C_MUTED, font=("Helvetica", 11),
            wraplength=860, justify="left",
        )
        desc.pack(anchor="w", padx=20, pady=(16, 4))

        body = self._panel(parent, "Resultados", C_Q1)
        self._q1_list = tk.Text(
            body, bg=C_PANEL, fg=C_TEXT,
            font=("Courier", 11), relief="flat",
            height=10, state="disabled",
        )
        self._q1_list.pack(fill="x")

        self._q1_bars = self._benchmark_bar(parent, C_Q1)

    def _fill_q1(self, r):
        self._q1_list.config(state="normal")
        self._q1_list.delete("1.0", "end")
        if not r.results:
            self._q1_list.insert("end", "  Sin resultados.\n")
        for i, m in enumerate(r.results, 1):
            amigos = ", ".join(f"{f['name']} ({f['rating']}★)"
                               for f in m.friends_who_watched)
            self._q1_list.insert("end",
                f"  {i}. {m.title} ({m.year})  —  promedio amigos: {m.avg_friend_rating}★\n"
                f"     Visto por: {amigos}\n\n"
            )
        self._q1_list.config(state="disabled")
        self._update_bars(self._q1_bars, r.benchmark.neo4j_ms, r.benchmark.postgres_ms)

    # ── Tab Q2 ────────────────────────────────────────────────

    def _build_q2_tab(self, parent):
        desc = tk.Label(
            parent,
            text=f"Actores a 2 grados de separación de Leonardo DiCaprio (actor {ACTOR_ID})",
            bg=C_PANEL, fg=C_MUTED, font=("Helvetica", 11),
        )
        desc.pack(anchor="w", padx=20, pady=(16, 4))

        body = self._panel(parent, "Resultados", C_Q2)
        self._q2_list = tk.Text(
            body, bg=C_PANEL, fg=C_TEXT,
            font=("Courier", 11), relief="flat",
            height=10, state="disabled",
        )
        self._q2_list.pack(fill="x")

        self._q2_bars = self._benchmark_bar(parent, C_Q2)

    def _fill_q2(self, r):
        self._q2_list.config(state="normal")
        self._q2_list.delete("1.0", "end")
        actor_x_name = r.actor_x['name'] if isinstance(r.actor_x, dict) else getattr(r.actor_x, 'name', '?')
        self._q2_list.insert("end",
            f"  Actor base: {actor_x_name}\n"
            f"  Total encontrados: {r.total_found}\n\n"
        )
        for i, a in enumerate(r.results[:10], 1):
            path = a.connection_path
            if path:
                item = path[0]
                actor = item['actor'] if isinstance(item, dict) else getattr(item, 'actor', '?')
                movie = item['movie'] if isinstance(item, dict) else getattr(item, 'movie', '?')
                puente = f"vía {actor} en '{movie}'"
            else:
                puente = ""
            self._q2_list.insert("end",
                f"  {i:>2}. {a.name:<30}  {puente}\n"
            )
        if r.total_found > 10:
            self._q2_list.insert("end", f"\n       ... y {r.total_found - 10} actores más\n")
        self._q2_list.config(state="disabled")
        self._update_bars(self._q2_bars, r.benchmark.neo4j_ms, r.benchmark.postgres_ms)

    # ── Tab Q3 ────────────────────────────────────────────────

    def _build_q3_tab(self, parent):
        desc = tk.Label(
            parent,
            text=f"Géneros nuevos para Carlos (user {USER_ID}) basados en calificaciones similares de Inception",
            bg=C_PANEL, fg=C_MUTED, font=("Helvetica", 11),
            wraplength=860, justify="left",
        )
        desc.pack(anchor="w", padx=20, pady=(16, 4))

        body = self._panel(parent, "Géneros sugeridos", C_Q3)

        self._q3_meta = tk.Label(body, text="", bg=C_PANEL, fg=C_MUTED,
                                  font=("Helvetica", 11), anchor="w")
        self._q3_meta.pack(fill="x", pady=(0, 8))

        self._q3_canvas = tk.Canvas(body, bg=C_PANEL, highlightthickness=0, height=220)
        self._q3_canvas.pack(fill="x")

        self._q3_bars = self._benchmark_bar(parent, C_Q3)

    def _fill_q3(self, r):
        self._q3_meta.config(
            text=f"Mis géneros: {', '.join(r.my_genres)}   |   "
                 f"Mi rating de {r.reference_movie['title']}: {r.reference_movie['my_rating']}★"
        )

        c = self._q3_canvas
        c.delete("all")

        if not r.suggested_genres:
            c.create_text(20, 20, text="Sin sugerencias.", fill=C_MUTED,
                          anchor="nw", font=("Helvetica", 11))
            self._update_bars(r.benchmark.neo4j_ms, r.benchmark.postgres_ms)
            return

        BAR_MAX = 340
        ROW_H   = 36
        colors  = [C_Q3, C_NEO4J, C_POSTGRES, C_Q1, C_Q2, "#e879f9", "#34d399"]

        for i, g in enumerate(r.suggested_genres):
            y = 10 + i * ROW_H
            color = colors[i % len(colors)]
            w = max(int(g.score * BAR_MAX), 6)

            c.create_text(4, y + ROW_H // 2,
                          text=f"{g.genre:<14}", fill=C_TEXT,
                          anchor="w", font=("Courier", 11, "bold"))
            c.create_rectangle(115, y + 6, 115 + BAR_MAX, y + ROW_H - 6,
                                fill=C_BG, outline="")
            c.create_rectangle(115, y + 6, 115 + w, y + ROW_H - 6,
                                fill=color, outline="")
            ejemplos = ", ".join(m["title"] for m in g.sample_movies[:2])
            info = f"score {g.score:.2f}  —  {ejemplos}" if ejemplos else f"score {g.score:.2f}"
            c.create_text(115 + BAR_MAX + 8, y + ROW_H // 2,
                          text=info, fill=C_MUTED,
                          anchor="w", font=("Helvetica", 10))

        c.config(height=10 + len(r.suggested_genres) * ROW_H + 10)
        self._update_bars(self._q3_bars, r.benchmark.neo4j_ms, r.benchmark.postgres_ms)

    # ── Ejecución async ───────────────────────────────────────

    def _run_async(self):
        """
        Corre las consultas en un hilo separado para no bloquear la UI.
        tkinter no es thread-safe para modificar widgets,
        por eso usamos after() para programar los updates en el hilo principal.
        """
        self.btn.config(state="disabled", text="⏳ Ejecutando...")
        self.status.config(text="Corriendo consultas...")
        threading.Thread(target=self._run_queries, daemon=True).start()

    def _run_queries(self):
        try:
            self.root.after(0, lambda: self.status.config(text="Q1 en curso..."))
            r1 = query_friends_movies(USER_ID, MIN_RATING)
            imprimir_q1(r1)
            self.root.after(0, lambda: self._fill_q1(r1))

            self.root.after(0, lambda: self.status.config(text="Q2 en curso..."))
            r2 = query_actor_network(ACTOR_ID)
            imprimir_q2(r2)
            self.root.after(0, lambda: self._fill_q2(r2))

            self.root.after(0, lambda: self.status.config(text="Q3 en curso..."))
            r3 = query_genre_suggestions(USER_ID, MOVIE_ID, TOLERANCE)
            imprimir_q3(r3)
            self.root.after(0, lambda: self._fill_q3(r3))

            self.root.after(0, lambda: self.status.config(text="✅ Listo"))
        except Exception as e:
            msg = str(e)
            self.root.after(0, lambda: self.status.config(text=f"❌ {msg}"))
            print(f"\n❌ Error: {e}")
        finally:
            self.root.after(0, lambda: self.btn.config(
                state="normal", text="▶  Ejecutar benchmarks"
            ))


# ══════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🚀 Inicializando conexiones...")
    init_pool()
    init_driver()

    print(f"\n📋 Configuración:")
    print(f"   Usuario de prueba : {USER_ID}  (Carlos Mendoza)")
    print(f"   Actor de prueba   : {ACTOR_ID}  (Leonardo DiCaprio)")
    print(f"   Película referencia: {MOVIE_ID}  (Inception)")

    root = tk.Tk()
    app  = BenchmarkApp(root)

    def on_close():
        print("\n🛑 Cerrando conexiones...")
        close_pool()
        close_driver()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    print("\n💡 Haz clic en '▶ Ejecutar benchmarks' en la ventana")
    print("   Los resultados también aparecerán aquí en consola.\n")

    root.mainloop()