from manim import *
import numpy as np

class HeavyMathShowcase(MovingCameraScene):
    def construct(self):
        # ---------- STYLING ----------
        self.camera.background_color = "#0c1736"
        AXIS_COLOR = GREY_B
        GRID_COLOR = BLUE_E
        ACCENT = YELLOW_A
        TEXT = WHITE

        # =========================================================
        # PART 1 — Linear Algebra: Matrix transform + eigenvectors
        # =========================================================
        title1 = Text("Linear Transform & Eigenvectors", color=TEXT).scale(0.6).to_edge(UP)
        self.add(title1)

        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            background_line_style={"stroke_color": GRID_COLOR, "stroke_width": 1},
            axis_config={"stroke_color": AXIS_COLOR, "stroke_width": 2},
        ).scale(1.0)
        axes_label = MathTex("x", ",", "y", color=TEXT).scale(0.6).to_corner(DL)
        self.add(plane, axes_label)

        # A non-trivial 2x2 matrix
        A = np.array([[2.0, -1.0],
                      [1.0,  0.5]])
        A_tex = MathTex(r"A=\begin{bmatrix}2 & -1\\ 1 & 0.5\end{bmatrix}", color=TEXT).scale(0.8)
        A_tex.to_corner(UR).shift(LEFT*0.2 + DOWN*0.2)
        self.play(FadeIn(A_tex, shift=UP, lag_ratio=0.1))

        # Show eigenvectors (computed with numpy)
        vals, vecs = np.linalg.eig(A)
        # Normalize just for drawing
        v1 = vecs[:, 0] / np.linalg.norm(vecs[:, 0])
        v2 = vecs[:, 1] / np.linalg.norm(vecs[:, 1])

        # Arrows at origin in eigenvector directions
        eig_v1 = Arrow(start=ORIGIN, end=np.array([v1[0], v1[1], 0])*2.5, color=ACCENT, buff=0)
        eig_v2 = Arrow(start=ORIGIN, end=np.array([v2[0], v2[1], 0])*2.5, color=GREEN_A, buff=0)

        eig_label1 = MathTex(r"v_1,\ \lambda_1=" + f"{vals[0]:.2f}", color=ACCENT).scale(0.6)
        eig_label2 = MathTex(r"v_2,\ \lambda_2=" + f"{vals[1]:.2f}", color=GREEN_A).scale(0.6)
        eig_label1.next_to(eig_v1.get_end(), UR, buff=0.2)
        eig_label2.next_to(eig_v2.get_end(), UL, buff=0.2)

        self.play(Create(eig_v1), FadeIn(eig_label1, shift=UP))
        self.play(Create(eig_v2), FadeIn(eig_label2, shift=UP))

        # A unit square + a random triangle to show deformation
        square = Square(side_length=1.8, color=YELLOW_D).move_to(LEFT*2 + DOWN*0.5)
        tri = Polygon(UP*1.0, RIGHT*1.2+DOWN*0.6, LEFT*1.2+DOWN*1.0, color=PINK)
        self.play(Create(square), Create(tri))

        # Apply the matrix to grid + shapes
        self.play(
            ApplyMatrix(A, plane, run_time=3, path_arc=0),
            ApplyMatrix(A, square, run_time=3, path_arc=0),
            ApplyMatrix(A, tri, run_time=3, path_arc=0),
            rate_func=rate_functions.ease_in_out_cubic
        )
        self.wait(0.4)

        # Subtle camera push-in to highlight deformation
        self.play(self.camera.frame.animate.scale(0.9).shift(RIGHT*0.4 + UP*0.2), run_time=2)
        self.wait(0.6)

        # =========================================================
        # PART 2 — Complex Analysis: Domain warping f(z) = z^2
        # =========================================================
        self.play(*[FadeOut(m, shift=DOWN*0.6) for m in [eig_v1, eig_v2, eig_label1, eig_label2, square, tri]])
        self.play(FadeOut(A_tex), run_time=0.6)

        title2 = Text("Complex Mapping:  f(z) = z^2", color=TEXT).scale(0.6).to_edge(UP)
        self.play(ReplacementTransform(title1, title2))

        # Fresh complex plane (thin grid looks better when warping)
        cplane = ComplexPlane(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            background_line_style={"stroke_color": GRID_COLOR, "stroke_width": 1},
            axis_config={"stroke_color": AXIS_COLOR, "stroke_width": 2},
        ).scale(1.2)
        cplane.add_coordinates()  # optional tick labels
        self.play(FadeTransform(plane, cplane), run_time=1.4)

        formula = MathTex(r"f(z)=z^2", color=TEXT).scale(0.9).to_corner(UR)
        self.play(FadeIn(formula, shift=UP*0.2))

        # A ring of sample points to watch how they move under f(z)=z^2
        pts = VGroup()
        R = 1.2
        for k in range(12):
            angle = 2*np.pi*k/12
            z = complex(R*np.cos(angle), R*np.sin(angle))
            dot = Dot(cplane.n2p(z), radius=0.05, color=YELLOW)
            pts.add(dot)
        self.play(FadeIn(pts, scale=0.8))

        # Animate the domain warping
        def f(z: complex) -> complex:
            return z**2

        # Show a smooth morph from identity to f(z)=z^2
        self.play(
            cplane.animate.apply_complex_function(f),
            pts.animate.apply_complex_function(f),
            run_time=4,
            rate_func=rate_functions.ease_in_out_cubic
        )
        self.wait(0.5)

        # Highlight angle doubling & radius squaring on one tracked point
        chosen = pts[0].copy().set_color(ACCENT)
        self.add(chosen)
        theta_label = MathTex(r"\text{angle} \mapsto 2\theta,\quad |z|\mapsto |z|^2", color=TEXT).scale(0.7)
        theta_label.to_corner(DL)
        self.play(FadeIn(theta_label, shift=UP*0.2))

        # Trace the path as we smoothly rotate the input z and remap through f
        tracer = TracedPath(chosen.get_center, stroke_width=2)
        self.add(tracer)

        # Parametric rotation in input plane, then mapped by f
        def rotate_and_map(mob, alpha):
            # rotate input z around origin, then map via f
            # start from angle 0 to 2π over the animation
            angle = 2*np.pi*alpha
            z0 = complex(R, 0.0)
            z_in = z0 * np.exp(1j*angle)
            z_out = f(z_in)
            mob.move_to(cplane.n2p(z_out))

        self.play(UpdateFromAlphaFunc(chosen, rotate_and_map), run_time=5, rate_func=linear)
        self.wait(0.6)

        # Outro
        box = Rectangle(width=6.4, height=0.9, color=WHITE).set_stroke(opacity=0.3)
        outro = Text("Linear Algebra + Complex Analysis = Visual Insight", color=WHITE).scale(0.6)
        grp = VGroup(box, outro).to_edge(DOWN)
        self.play(FadeIn(grp, shift=UP*0.2))
        self.wait(1.5)
