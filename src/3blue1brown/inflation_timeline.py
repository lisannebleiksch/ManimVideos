# manim -pql inflation_travel.py TimelineFlythroughToInflation
from manim import *
import math


class TimelineZoomInflation(MovingCameraScene):
    def construct(self):
        # --------- TIME BOUNDS (seconds) ----------
        T_MIN = 1e-44
        T_MAX = 4.355e17   # ~13.8 Gyr

        # Key epochs (approx seconds after Big Bang)
        T_INFL_START = 1e-36
        T_INFL_END   = 1e-32
        T_PLANCK     = 1e-43
        T_BARYOGEN   = 1e-6      # illustrative
        T_QCD        = 1e-5      # illustrative
        T_BBN        = 180       # ~3 minutes
        T_RECOMB     = 3.8e5 * 365.25 * 24 * 3600  # ~380k yr
        T_TODAY      = T_MAX

        # --------- LAYOUT / TUNING ----------
        axis_width = 24.0
        axis_y     = -1.0
        tick_h     = 0.16

        # Readability knobs
        PING_FONT      = 0.54   # callout font scale
        PING_DY        = 0.80   # callout vertical offset
        PING_LINGER    = 1.00   # how long labels stay visible at waypoints (sec)
        PING_FADE      = 0.25   # fade-out time (sec)
        TRAVEL_RT      = 1.35   # camera travel time between waypoints (sec)
        START_WIDTH    = 6.5    # initial camera width
        NEAR_WIDTH     = 3.4    # width near inflation mid
        TIGHT_WIDTH    = 2.2    # final tight zoom width

        # ---------- LOG MAP ----------
        log_min = math.log10(T_MIN)
        log_max = math.log10(T_MAX)
        def x_of_t(t):
            lt = math.log10(t)
            u = (lt - log_min) / (log_max - log_min)
            return -axis_width/2 + u * axis_width

        # ---------- AXIS ----------
        axis = Line(LEFT*axis_width/2, RIGHT*axis_width/2).move_to([0, axis_y, 0])

        ticks = VGroup()
        labels = VGroup()
        for d in range(-44, 19, 4):
            td = 10**d
            if td < T_MIN or td > T_MAX:
                continue
            x = x_of_t(td)
            ticks.add(Line([x, axis_y - tick_h, 0], [x, axis_y + tick_h, 0], stroke_width=1.5, color=GRAY_B))
            lbl = MarkupText(f"10<sup>{d}</sup> s").scale(0.38).set_color(GRAY_B)
            lbl.move_to([x, axis_y - 0.55, 0])
            # Subtle background for tick labels too
            lbl_bg = BackgroundRectangle(lbl, fill_opacity=0.35, buff=0.02, color=BLACK)
            labels.add(VGroup(lbl_bg, lbl))

        title = Text("Cosmic Time (log seconds)").scale(0.62).to_edge(UP)
        title_bg = BackgroundRectangle(title, fill_opacity=0.35, buff=0.08, color=BLACK)

        # Inflation band
        infl_band = Rectangle(
            width  = x_of_t(T_INFL_END) - x_of_t(T_INFL_START),
            height = 0.36, stroke_width=0,
            fill_color=YELLOW, fill_opacity=0.25
        ).move_to([(x_of_t(T_INFL_START)+x_of_t(T_INFL_END))/2, axis_y, 0])

        self.play(
            FadeIn(VGroup(title_bg, title), shift=UP*0.2),
            Create(axis),
            LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.02),
            FadeIn(labels),
            run_time=1.6
        )

        # ---------- CAMERA HELPERS ----------
        frame = self.camera.frame
        def focus_on(t, width, rt=1.0, ease=smooth):
            x = x_of_t(t)
            self.play(frame.animate.move_to([x, axis_y, 0]).set_width(width), run_time=rt, rate_func=ease)

        def ping(text, t, color=WHITE):
            """Minimal readable callout with background."""
            x = x_of_t(t)
            dot = Dot([x, axis_y, 0], radius=0.04, color=color)
            lbl = Text(text).scale(PING_FONT).set_color(color).move_to([x, axis_y+PING_DY, 0])
            lbl_bg = BackgroundRectangle(lbl, fill_opacity=0.60, buff=0.08, color=BLACK)
            grp = VGroup(dot, lbl_bg, lbl).set_z_index(10)
            self.play(FadeIn(dot, scale=0.5), FadeIn(lbl_bg), FadeIn(lbl, shift=UP*0.1), run_time=0.45)
            return grp

        # ---------- START AT TODAY ----------
        focus_on(T_TODAY, width=START_WIDTH, rt=0.9)
        today_tag = ping("Today (~13.8 Gyr)", T_TODAY, color=GREEN_B)
        self.wait(0.35)

        # ---------- GLIDE LEFT WITH LONGER HOLDS ----------
        waypoints = [
            (T_RECOMB,  START_WIDTH, "Recombination (CMB)", TEAL_B),
            (T_BBN,     5.6,         "Big Bang Nucleosynthesis", BLUE_B),
            (T_QCD,     5.0,         "QCD transition", PURPLE_B),
            (T_BARYOGEN,4.6,         "Baryogenesis", MAROON_B),
            (T_PLANCK,  4.0,         "Planck time", BLUE_C),
        ]

        # Keep the previous tag visible a bit while we move; fade it as we arrive at the next
        prev_tag = today_tag
        for (t, w, label, col) in waypoints:
            self.play(frame.animate.move_to([x_of_t(t), axis_y, 0]).set_width(w), run_time=TRAVEL_RT, rate_func=smooth)
            # let previous linger while arriving
            self.wait(0.15)
            # fade previous out gently
            self.play(FadeOut(prev_tag, run_time=PING_FADE))
            tag = ping(label, t, color=col)
            self.wait(PING_LINGER)
            prev_tag = tag

        # --- ARRIVE & HOLD AT INFLATION (clean, non-overlapping) ---
        self.play(FadeOut(labels, run_time=0.3))  # hide global labels

        self.play(FadeIn(infl_band), run_time=0.6)

        t_mid = math.sqrt(T_INFL_START * T_INFL_END)

        # Zoom in but keep enough width so text isn't huge
        self.play(
            self.camera.frame.animate
                .move_to([x_of_t(t_mid), axis_y + 0.15, 0])  # small upward shift
                .set_width(3.4),                              # wider view to avoid blow-up
            run_time=1.0, rate_func=smooth
        )

        # Arrows only (no small labels here)
        start_arrow = Arrow(
            start=[x_of_t(T_INFL_START), axis_y+0.28, 0],
            end=[x_of_t(T_INFL_START),   axis_y+0.08, 0], buff=0
        ).set_color(YELLOW_B)
        end_arrow = Arrow(
            start=[x_of_t(T_INFL_END), axis_y+0.28, 0],
            end=[x_of_t(T_INFL_END),   axis_y+0.08, 0], buff=0
        ).set_color(YELLOW_B)

        # Big clean top numbers
        # Big clean top numbers (slightly smaller now)
        top_left  = MarkupText("10<sup>-36</sup> s").scale(0.65).set_color(YELLOW_B)
        top_right = MarkupText("10<sup>-32</sup> s").scale(0.65).set_color(YELLOW_B)

        top_y = self.camera.frame.get_top()[1] - 0.5
        top_left.move_to([x_of_t(T_INFL_START), top_y, 0])
        top_right.move_to([x_of_t(T_INFL_END),   top_y, 0])
        tl_bg = BackgroundRectangle(top_left,  fill_opacity=0.55, buff=0.08, color=BLACK)
        tr_bg = BackgroundRectangle(top_right, fill_opacity=0.55, buff=0.08, color=BLACK)
        top_left_group  = VGroup(tl_bg, top_left)
        top_right_group = VGroup(tr_bg, top_right)

        # Centered "Inflation period" smaller, lower on the band
        infl_txt = Text("Inflation period").scale(0.5).set_color(WHITE)
        infl_bg  = BackgroundRectangle(infl_txt, fill_opacity=0.55, buff=0.10, color=BLACK)
        infl_label = VGroup(infl_bg, infl_txt).next_to(infl_band, DOWN, buff=0.15)

        # Animate cleanly
        self.play(GrowArrow(start_arrow), GrowArrow(end_arrow), run_time=0.6)
        self.play(FadeIn(top_left_group), FadeIn(top_right_group), FadeIn(infl_label), run_time=0.6)

        self.wait(2.0)
