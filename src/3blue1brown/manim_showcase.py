from manim import *
import numpy as np

# ===== 1) 3D: Parametrische oppervlakte + camera orbit =====
class Showcase3D(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#0c1736"
        axes = ThreeDAxes(x_range=(-3, 3, 1), y_range=(-3, 3, 1), z_range=(-2, 2, 1))
        title = Text("3D Parametric Surface + Camera", color=WHITE).scale(0.5).to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.set_camera_orientation(phi=60*DEGREES, theta=-30*DEGREES)

        def surface_func(u, v):
            # Een zachte golf (“ripple”) op z = sin(r)/r
            r = np.sqrt(u*u + v*v) + 1e-6
            z = 0.8 * np.sin(3*r) / r
            return np.array([u, v, z])

        surf = Surface(
            surface_func,
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(36, 36),
            checkerboard_colors=[BLUE_E, BLUE_D],
            stroke_color=BLUE_E,
        )
        self.add(axes)
        self.play(FadeIn(surf, shift=IN), run_time=1.5)
        # Camera-orbit om het 3D-gevoel te tonen
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(surf), FadeOut(axes), run_time=1)

# ===== 2) Vectorveld: pijlen + streamlines met animatie =====
class ShowcaseFields(Scene):
    def construct(self):
        self.camera.background_color = "#0c1736"
        title = Text("Vector Field + StreamLines", color=WHITE).scale(0.5).to_edge(UP)
        self.add(title)

        plane = NumberPlane(
            x_range=[-4, 4, 1], y_range=[-3, 3, 1],
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1},
            axis_config={"stroke_color": GREY_B, "stroke_width": 2},
        )
        self.add(plane)

        def F(point):
            # Een roterend/spiralerend veld
            x, y = point[0], point[1]
            return np.array([y - 0.5*x, -x - 0.2*y, 0])

        field = ArrowVectorField(F, x_range=[-4, 4], y_range=[-3, 3], colors=[BLUE_B, YELLOW_A])
        self.play(FadeIn(field), run_time=1)

        sl = StreamLines(
            F,
            x_range=[-4, 4], y_range=[-3, 3],
            padding=1, stroke_width=2, opacity=0.9,
        )
        self.play(Create(sl), run_time=2)
        self.wait(2)

        # Dots die over de streamlines “meegliden”
        sl.start_animation(warm_up=False, flow_speed=1.0)
        self.wait(3)
        sl.stop_animation()
        self.play(FadeOut(sl), FadeOut(field), FadeOut(plane), run_time=1)

# ===== 3) Grafen: netwerk + kortste pad highlight =====
class ShowcaseGraphs(Scene):
    def construct(self):
        self.camera.background_color = "#0c1736"
        title = Text("Graph Animation + Shortest Path Highlight", color=WHITE).scale(0.5).to_edge(UP)
        self.add(title)

        # Nodes op vaste posities (hex-achtige layout)
        vertices = list(range(1, 10))
        layout = {
            1: (-3, 1, 0), 2: (-1.5, 2, 0), 3: (0, 1, 0),
            4: (-3, -1, 0), 5: (-1.5, 0, 0), 6: (0, -1, 0),
            7: (1.5, 1.5, 0), 8: (1.5, -0.5, 0), 9: (3, 0.5, 0),
        }
        edges = [
            (1,2),(2,3),(1,4),(2,5),(3,6),
            (4,5),(5,6),(3,7),(6,8),(7,9),(8,9),(5,7),(5,8)
        ]

        g = Graph(
            vertices, edges, layout=layout,
            vertex_config={"fill_color": BLUE_D, "radius": 0.18},
            edge_config={"stroke_color": GREY_B},
            labels=True
        )
        self.play(Create(g), run_time=2)

        start, goal = 1, 9
        # Simpele “handmatige” kortste pad in dit kleine graafje:
        shortest_path = [1, 2, 5, 7, 9]

        # Highlight het pad
        path_edges = list(zip(shortest_path, shortest_path[1:]))
        highlight = VGroup(*[
            g.edges[e].copy().set_stroke(YELLOW_A, width=6) for e in path_edges
        ])
        self.play(LaggedStart(*[Indicate(g[v], color=YELLOW_A) for v in shortest_path], lag_ratio=0.2))
        self.play(Create(highlight), run_time=1.5)
        self.wait(1.5)
        self.play(FadeOut(highlight), FadeOut(g), run_time=1)

# ===== 4) LaTeX: nette afleiding met TransformMatchingTex =====
class ShowcaseMathText(Scene):
    def construct(self):
        self.camera.background_color = "#0c1736"
        title = Text("TransformMatchingTex: Clean Algebra Steps", color=WHITE).scale(0.5).to_edge(UP)
        self.add(title)

        eq1 = MathTex(r"(x+1)^2 = x^2 + 2x + 1", color=WHITE).scale(1.1)
        eq2 = MathTex(r"x^2 + 2x + 1 - 4 = 0", color=WHITE).scale(1.1)
        eq3 = MathTex(r"x^2 + 2x - 3 = 0", color=WHITE).scale(1.1)
        eq4 = MathTex(r"(x+3)(x-1)=0", color=WHITE).scale(1.1)
        eq5 = MathTex(r"x\in\{-3,\,1\}", color=YELLOW_A).scale(1.1)

        VGroup(eq1, eq2, eq3, eq4, eq5).arrange(DOWN, buff=0.7).move_to(ORIGIN)

        self.play(Write(eq1))
        self.wait(0.6)
        self.play(TransformMatchingTex(eq1.copy(), eq2))
        self.wait(0.4)
        self.play(TransformMatchingTex(eq2.copy(), eq3))
        self.wait(0.4)
        self.play(TransformMatchingTex(eq3.copy(), eq4))
        self.wait(0.4)
        self.play(TransformMatchingTex(eq4.copy(), eq5))
        self.wait(1.2)
        self.play(*[FadeOut(m) for m in [eq1, eq2, eq3, eq4, eq5, title]])

# ===== 5) Updaters: live teller + punt dat f(t) volgt =====
class ShowcaseUpdaters(Scene):
    def construct(self):
        self.camera.background_color = "#0c1736"
        title = Text("Updaters: Live Counter + Motion on Curve", color=WHITE).scale(0.5).to_edge(UP)
        self.add(title)

        # Sine-curve
        ax = Axes(x_range=[0, 8, 1], y_range=[-2, 2, 1],
                  axis_config={"stroke_color": GREY_B, "stroke_width": 2},
                  tips=False).to_edge(DOWN, buff=1)
        curve = ax.plot(lambda x: 1.2*np.sin(1.5*x)*np.exp(-0.12*x), x_range=[0, 8], stroke_width=4, color=BLUE_D)
        self.play(Create(ax), Create(curve), run_time=1.5)

        # Dot dat over de curve beweegt o.b.v. tijd
        dot = Dot(color=YELLOW_A, radius=0.09)
        t_tracker = ValueTracker(0)

        def move_dot(mob):
            t = t_tracker.get_value()
            x = t
            y = 1.2*np.sin(1.5*x)*np.exp(-0.12*x)
            mob.move_to(ax.c2p(x, y))

        dot.add_updater(move_dot)
        self.add(dot)

        # Live teller met updater
        counter = DecimalNumber(0, color=WHITE, num_decimal_places=2).scale(0.9)
        counter.to_corner(UR)
        counter.add_updater(lambda m: m.set_value(t_tracker.get_value()))
        self.add(counter)

        # Animeren van t
        self.play(t_tracker.animate.set_value(8), run_time=5, rate_func=linear)
        dot.remove_updater(move_dot)
        counter.remove_updater(lambda m: m.set_value(t_tracker.get_value()))
        self.wait(0.6)
        self.play(FadeOut(dot), FadeOut(curve), FadeOut(ax), FadeOut(counter), FadeOut(title))
