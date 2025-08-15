# manim -pqh inflation_compare.py ScaleComparisons_NoTex
from manim import *
import math

class ScaleComparisons_NoTex(Scene):
    def construct(self):
        BG = "#0c1736"
        ACCENT = YELLOW_A
        self.camera.background_color = BG

        TOTAL = 8.0          # total seconds for the stretch
        SCALE_START = 1.0
        SCALE_END   = 1e26
        W_MIN, W_MAX = 2.0, 12.0
        BAR_H = 0.16

        title = Text("What does ×10^26 mean?", weight=BOLD).scale(0.8).to_edge(UP)
        self.add(title)

        scale_tracker = ValueTracker(SCALE_START)

        def width_for_scale(s):
            # map scale factor to visual width (log interpolation)
            t = (math.log10(s) - math.log10(SCALE_START)) / (math.log10(SCALE_END) - math.log10(SCALE_START))
            t = max(0.0, min(1.0, t))
            t = smooth(t)
            return W_MIN + (W_MAX - W_MIN) * t

        # Row builder: label + bar + result label (hidden until end)
        def make_row(left_text, result_text):
            bar = always_redraw(lambda: Rectangle(
                width=width_for_scale(scale_tracker.get_value()),
                height=BAR_H,
                fill_opacity=1.0,
                color=BLUE_E,
                stroke_width=0,
            ))
            result_label = Text(result_text).scale(0.45).set_color(ACCENT).set_opacity(0.0)
            group = VGroup(Text(left_text).scale(0.5).set_color(WHITE), bar, result_label) \
                .arrange(RIGHT, buff=0.4)
            return group, result_label

        row1, res_label1 = make_row("1 nm × 10^26", "~10 light-years")
        row2, res_label2 = make_row("proton (~10^-15 m) × 10^26", "~1 AU (Earth–Sun)")

        rows = VGroup(row1, row2).arrange(DOWN, buff=0.9).next_to(title, DOWN, buff=0.8).to_edge(LEFT, buff=1.0)
        self.add(rows)

        # Animate the scaling on log scale
        def drive(alpha):
            logv = interpolate(0, 26, alpha)
            scale_tracker.set_value(10 ** logv)

        self.play(UpdateFromAlphaFunc(rows, lambda _m, a: drive(a)), run_time=TOTAL, rate_func=linear)

        # Fade in results
        self.play(res_label1.animate.set_opacity(1.0), res_label2.animate.set_opacity(1.0), run_time=0.6)
        self.wait(0.5)
