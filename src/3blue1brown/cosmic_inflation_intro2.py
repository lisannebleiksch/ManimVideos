from __future__ import annotations
import numpy as np
from manim import *

class InflationGridIntro2(MovingCameraScene):
    def construct(self):
        # ---------- Parameters ----------
        N = 6              # half grid size in cells (comoving)
        cell = 0.5         # comoving cell size
        H = 0.9            # inflation "Hubble" rate (per sec of animation time)
        T_INF = 5.0        # seconds of exponential inflation
        k = 0.5            # post-inflation linear factor
        p = 0.6            # post-inflation power
        T_TOTAL = 10.0     # total animation seconds

        # ---------- Time / scale factor ----------
        tau = ValueTracker(0.0)

        def a(t: float) -> float:
            """Piecewise scale factor a(τ)."""
            if t <= T_INF:
                return np.exp(H * t)
            a_inf = np.exp(H * T_INF)
            return a_inf * (1 + k * (t - T_INF)) ** p

        # convenient: an updater-visible a(τ)
        def a_now() -> float:
            return a(tau.get_value())

        # ---------- Background stars (parallax-lite) ----------
        # Stars that do NOT scale with a(τ), to sell the "we zoom through" vibe.
        rng = np.random.default_rng(42)
        stars_xy = rng.uniform(-7, 7, size=(300, 2))
        stars = VGroup(*[Dot(point=[x, y, -2], radius=0.015, color=GRAY_E, fill_opacity=0.6)
                         for x, y in stars_xy])
        stars.set_z_index(-5)

        # ---------- Comoving grid lines & points (scale with a) ----------
        # Build as functions of integer coordinates; use always_redraw so they follow a(τ).
        # Grid lines:
        x_coords = np.arange(-N, N + 1) * cell
        y_coords = np.arange(-N, N + 1) * cell

        def phys(xy):
            """Map comoving coord to physical position by multiplying with a(τ)."""
            return np.array([xy[0] * a_now(), xy[1] * a_now(), 0.0])

        def make_vline(xc):
            return always_redraw(lambda: Line(
                phys((xc, -N * cell)), phys((xc, N * cell)),
                stroke_width=1.5, stroke_opacity=0.35, color=BLUE_E
            ).set_z_index(-1))

        def make_hline(yc):
            return always_redraw(lambda: Line(
                phys((-N * cell, yc)), phys((N * cell, yc)),
                stroke_width=1.5, stroke_opacity=0.35, color=BLUE_E
            ).set_z_index(-1))

        vlines = VGroup(*[make_vline(xc) for xc in x_coords])
        hlines = VGroup(*[make_hline(yc) for yc in y_coords])

        # Comoving lattice points (dots):
        def make_dot(i, j):
            if i == 0 and j == 0:
                color = YELLOW_B
                r = 0.05
            else:
                color = TEAL_B
                r = 0.035
            return always_redraw(
                lambda i=i, j=j: Dot(
                    point=phys((i * cell, j * cell)),
                    radius=r, color=color, fill_opacity=1.0
                ).set_z_index(1)
            )

        dots = VGroup(*[
            make_dot(i, j)
            for i in range(-N, N + 1)
            for j in range(-N, N + 1)
        ])

        # ---------- Hubble patches (constant comoving radii) ----------
        r1_c, r2_c = 1.0 * cell * (N / 2), 2.0 * cell * (N / 2)
        def make_patch(r_c, color):
            return always_redraw(lambda: Circle(
                radius=r_c * a_now(), color=color, stroke_opacity=0.6, stroke_width=2
            ).set_z_index(0))
        patch1 = make_patch(r1_c, color=PURPLE_B)
        patch2 = make_patch(r2_c, color=PURPLE_D)

        # Labels for patches
        def make_patch_label(y_shift, txt):
            return always_redraw(lambda: Text(
                txt, font_size=28, color=PURPLE_B
            ).next_to(ORIGIN, UP, buff=0.2).shift(y_shift).set_z_index(2))
        patch_lbl = make_patch_label(UP*0.7, "Hubble patch (comoving radius fixed)")

        # ---------- Scale factor indicator & timeline ----------
        # Temporarily replaced MathTex with Text due to LaTeX dependency issue
        a_label = always_redraw(lambda: Text(
            "a(τ) = exp(H·τ) (inflation) or a(T_inf)·[1+k(τ-T_inf)]^p (radiation)",
            font_size=20, color=WHITE
        ).scale(0.5).to_corner(UL).set_z_index(3))

        a_value = always_redraw(lambda: Text(
            f"{a_now():.2f}", font_size=32, color=YELLOW_B
        ).scale(0.8).next_to(a_label, DOWN, buff=0.2).set_z_index(3))

        # Progress bar
        bar_w = 6
        bar_bg = Rectangle(width=bar_w, height=0.12, fill_opacity=0.2, fill_color=GRAY_D, stroke_width=0)
        bar_bg.to_edge(DOWN).shift(DOWN*0.3).set_z_index(3)
        bar_fg = always_redraw(lambda: Rectangle(
            width=bar_w * (tau.get_value() / T_TOTAL),
            height=0.12,
        ).set_fill(color=WHITE, opacity=0.9).set_stroke(width=0).align_to(bar_bg, LEFT).move_to(
            bar_bg.get_left() + RIGHT * (bar_w * (tau.get_value() / (2*T_TOTAL)))
        ).to_edge(DOWN).shift(DOWN*0.3).set_z_index(3))

        # ---------- Camera setup ----------
        self.camera.frame.save_state()
        self.camera.frame.set_width(8)

        # ---------- Build scene ----------
        self.add(stars)
        self.play(FadeIn(vlines), FadeIn(hlines), FadeIn(dots), FadeIn(patch1), FadeIn(patch2), FadeIn(patch_lbl))
        self.play(FadeIn(a_label), FadeIn(a_value), FadeIn(bar_bg), FadeIn(bar_fg))

        # Phase 1: inflation (exponential growth)
        # As objects blow up, zoom out a bit to keep context.
        self.play(
            tau.animate.set_value(T_INF),
            self.camera.frame.animate.set_width(10),
            run_time=T_INF,
            rate_func=smooth
        )

        # Phase 2: slower expansion
        self.play(
            tau.animate.set_value(T_TOTAL),
            self.camera.frame.animate.set_width(11.5),
            run_time=T_TOTAL - T_INF,
            rate_func=lambda t: t  # linear
        )

        self.wait(0.5)
        self.play(self.camera.frame.animate.restore(), run_time=1.0)
        self.wait(0.3)
