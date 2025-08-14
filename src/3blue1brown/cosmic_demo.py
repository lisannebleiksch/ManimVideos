from manim import *
import math

# ---------- Scene 1: Expanderend "ruimte"-grid ----------
class ExpandingGrid(Scene):
    def construct(self):
        self.camera.background_color = "#0c1020"  # deep space

        # Grid als referentie voor "ruimte"
        grid = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-3.5, 3.5, 1],
            background_line_style={"stroke_opacity": 0.25, "stroke_width": 1},
            axis_config={"stroke_opacity": 0.0}
        )
        grid.set_color("#60a5fa")  # lichtblauw
        self.add(grid)

        # "Galaxies" als dots op vaste gridpunten (co-movende observables)
        points = VGroup(
            *[Dot(point=[x, y, 0], radius=0.06, color="#fbbf24")
              for x, y in [(-3, -1), (0, 0), (2, 1), (4, -1), (-1, 2)]]
        )
        self.add(points)

        title = Text("Cosmic Inflation", weight=BOLD).scale(0.9).to_edge(UP)
        title.set_color("#ffffff")
        self.play(FadeIn(title, shift=UP), run_time=0.8)

        # Scale‑animatie voor "ruimte zet uit"
        self.play(
            grid.animate.scale(1.8),
            points.animate.scale(1.8),
            run_time=2.0,
            rate_func=smooth
        )

        # Nog verder uitzetten (sneller) en dan vertragen
        self.play(
            AnimationGroup(
                grid.animate.scale(1.5),
                points.animate.scale(1.5),
                lag_ratio=0.0
            ),
            run_time=1.2,
            rate_func=rush_from
        )
        self.wait(0.4)

        # Langzaam stabiliseren
        self.play(
            grid.animate.scale(1.1),
            points.animate.scale(1.1),
            run_time=1.2,
            rate_func=there_and_back_with_pause
        )
        self.play(FadeOut(title, shift=UP), run_time=0.6)
        self.wait(0.2)

# ---------- Scene 2: (Fictieve) schaalfactor a(t) ----------
class ScaleFactorPlot(Scene):
    def construct(self):
        self.camera.background_color = "#0c1020"

        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 6, 1],
            x_length=10,
            y_length=5,
            tips=False,
            axis_config={"stroke_color": "#94a3b8", "stroke_width": 2},
        ).to_edge(DOWN)
        labels = VGroup(
            Text("time", color="#ffffff").scale(0.4).next_to(axes.x_axis, DOWN, buff=0.2),
            Text("a(t)", color="#ffffff").scale(0.4).next_to(axes.y_axis, LEFT, buff=0.2),
        )

        self.play(Create(axes), FadeIn(labels), run_time=0.8)

        # Fictieve a(t): eerst super‑exponentieel (inflation), dan trager
        def a_of_t(t: float) -> float:
            if t < 2.0:
                return 0.2 * math.exp(1.5 * t)   # snelle expansie
            else:
                return 0.2 * math.exp(1.5 * 2.0) + 0.8 * (t - 2.0)  # lineair trager

        graph = axes.plot(a_of_t, x_range=[0, 6], color="#22d3ee", stroke_width=6)
        glow = graph.copy().set_stroke(width=16, opacity=0.25)

        title = Text("Scale factor a(t)", weight=BOLD, color="#ffffff").to_edge(UP)

        self.play(FadeIn(title, shift=UP), run_time=0.6)
        self.play(Create(glow), run_time=0.6)
        self.play(Create(graph), run_time=1.4, rate_func=smooth)

        # Markeer de "inflation" fase
        brace = BraceBetweenPoints(
            axes.c2p(0.0, a_of_t(0.0)),
            axes.c2p(2.0, a_of_t(2.0)),
            color="#f97316"
        )
        label = Text("inflation era", color="#f97316").scale(0.5).next_to(brace, UP, buff=0.15)

        self.play(GrowFromCenter(brace), FadeIn(label, shift=UP), run_time=0.8)
        self.wait(0.6)

        # Fade out
        self.play(FadeOut(VGroup(brace, label, glow, graph, labels, axes, title)))
        self.wait(0.2)
