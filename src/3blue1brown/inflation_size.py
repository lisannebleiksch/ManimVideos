# manim -pqh inflation_compare.py ScaleComparisons_NoTex
from manim import *
import math

class ScaleComparisons_NoTex(Scene):
    def construct(self):
        # --- Look & feel ---
        BG = "#0c1736"
        ACCENT = YELLOW_A
        self.camera.background_color = BG

        TOTAL = 8.0          # total seconds
        SCALE_START = 1.0    # conceptual scale start
        SCALE_END   = 1e26   # conceptual scale end (we map to a visual width)
        W_MIN, W_MAX = 2.0, 12.0  # visual bar widths in scene units
        BAR_H = 0.16

        title = Text("What does ×10^26 mean?", weight=BOLD).scale(0.8).to_edge(UP)
        self.add(title)

        # Tracker drives both rows' bar widths
        scale_tracker = ValueTracker(SCALE_START)

        # Helper: map conceptual scale (1..1e26) to width (W_MIN..W_MAX) with smooth log progression
        def width_for_scale(s):
            t = (math.log10(s) - math.log10(SCALE_START)) / (math.log10(SCALE_END) - math.log10(SCALE_START))
            t = max(0.0, min(1.0, t))
            t = smooth(t)
            return W_MIN + (W_MAX - W_MIN) * t

        # ----- Row component (label + animated bar + result) -----
        def make_row(left_label: Mobject, result_text: str):
            # bar is re-created every frame based on scale_tracker
            bar = always_redraw(lambda: Rectangle(
                width=width_for_scale(scale_tracker.get_value()),
                height=BAR_H,
                fill_opacity=1.0,
                color=BLUE_E,
                stroke_width=0,
            ))
            # Layout: [left label]   [bar]   [right placeholder (appears at end)]
            right = MarkupText(result_text).scale(0.5).set_color(ACCENT)
            group = VGroup(left_label.scale(0.52), bar, right.set_opacity(0.0)).arrange(RIGHT, buff=0.4)
            return group, bar, right

        # Row 1: nanometer → ~10 ly
        left1 = MarkupText("1 nm × 10<sup>26</sup>").set_color(WHITE)
        res1  = "~10 light-years"
        row1, bar1, right1 = make_row(left1, res1)

        # Row 2: proton (~10^-15 m) → ~1 AU
        left2 = MarkupText("proton (~10<sup>-15</sup> m) × 10<sup>26</sup>").set_color(WHITE)
        res2  = "~1 AU (Earth–Sun)"
        row2, bar2, right2 = make_row(left2, res2)

        rows = VGroup(row1, row2).arrange(DOWN, buff=0.9).next_to(title, DOWN, buff=0.8).to_edge(LEFT, buff=1.0)
        self.add(rows)

        # Counter tag (optional, top-right): ×10^k
        def counter():
            k = int(round(math.log10(max(1.0, scale_tracker.get_value()))))
            return MarkupText(f"×10<sup>{k}</sup>").scale(0.7).set_color(ACCENT).to_corner(UR, buff=0.5)
        count_tag = always_redraw(counter)
        self.add(count_tag)

        # Animate the scale up (log feel)
        def drive(alpha):
            # animate on log scale: 1 -> 1e26
            logv = interpolate(0, 26, alpha)  # decades
            scale_tracker.set_value(10 ** logv)

        self.play(UpdateFromAlphaFunc(rows, lambda _m, a: drive(a)), run_time=TOTAL, rate_func=linear)

        # Pop in the results with braces under bars
        brace1 = Brace(bar1, direction=DOWN, buff=0.12)
        note1 = brace1.get_text(res1).scale(0.55).set_color(ACCENT)
        brace2 = Brace(bar2, direction=DOWN, buff=0.12)
        note2 = brace2.get_text(res2).scale(0.55).set_color(ACCENT)

        self.play(
            right1.animate.set_opacity(1.0),
            right2.animate.set_opacity(1.0),
            run_time=0.4,
        )
        self.play(GrowFromCenter(brace1), FadeIn(note1, shift=DOWN*0.15), run_time=0.6)
        self.play(GrowFromCenter(brace2), FadeIn(note2, shift=DOWN*0.15), run_time=0.6)
        self.wait(0.6)
