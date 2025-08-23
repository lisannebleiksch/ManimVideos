# manim -pqh zoom_ladder_v2.py ZoomLadder_NoTex_V2
from manim import *
import math

class ZoomLadder_NoTex_V2(MovingCameraScene):
    def construct(self):
        USE_GREENSCREEN = False
        USE_TRANSPARENT = True
        BG = "#0c1736"
        KEY = "#00FF00"
        ACCENT = YELLOW_A
        
        # Choose background: transparent, green screen, or normal
        if USE_TRANSPARENT:
            self.camera.background_color = "#00000000"  # Fully transparent
        elif USE_GREENSCREEN:
            self.camera.background_color = KEY
        else:
            self.camera.background_color = BG

        CAMERA_WIDTH = 12.0   # ← wider = less zoom
        TRACK_H = 0.6
        CARD_ICON_H = 1.2
        CARD_SPACING = 3.0

        # --- simple icons (kept small & consistent) ---
        def ic_nm():
            return RoundedRectangle(width=0.6, height=0.14, corner_radius=0.07,
                                    fill_opacity=1, fill_color=BLUE_E, stroke_width=0)
        def ic_bact():
            c = Circle(radius=0.5, color=TEAL_B, fill_opacity=0.6, stroke_width=2)
            return VGroup(c, Dot(radius=0.06, color=WHITE).shift(LEFT*0.12+UP*0.05))
        def ic_human():
            head = Circle(radius=0.16, color=WHITE, stroke_width=2)
            body = Line(ORIGIN, DOWN*0.8, stroke_width=2).next_to(head, DOWN, buff=0.02)
            arms = Line(LEFT*0.45, RIGHT*0.45, stroke_width=2).next_to(head, DOWN, buff=0.22)
            legs = VGroup(Line(ORIGIN, DOWN*0.45+LEFT*0.25, stroke_width=2),
                          Line(ORIGIN, DOWN*0.45+RIGHT*0.25, stroke_width=2)).next_to(body, DOWN, buff=0)
            return VGroup(head, body, arms, legs)
        def ic_earth():
            g = Circle(radius=0.5, color=BLUE_B, fill_opacity=0.8)
            land = VGroup(Dot(radius=0.10, color=GREEN_B).shift(LEFT*0.12+UP*0.08),
                          Dot(radius=0.08, color=GREEN_B).shift(RIGHT*0.18+DOWN*0.05))
            return VGroup(g, land)
        def ic_solar():
            sun = Dot(radius=0.10, color=YELLOW_B)
            orbs = VGroup(*[Circle(radius=r, color=GREY_B, stroke_opacity=0.6) for r in (0.45, 0.85, 1.2)])
            return VGroup(orbs, sun)
        def ic_oort():
            core = Dot(radius=0.05, color=YELLOW_B)
            shell = Circle(radius=1.2, color=GREY_B, stroke_opacity=0.4)
            dots = VGroup(*[Dot(color=GREY_B, radius=0.02).move_to(shell.point_at_angle(a))
                            for a in [i*TAU/22 for i in range(22)]])
            return VGroup(shell, dots, core)
        def ic_stars():
            a = RegularPolygon(5).scale(0.45).set_stroke(WHITE, 2)
            b = RegularPolygon(4).scale(0.3).set_stroke(WHITE, 2).shift(RIGHT*0.7+UP*0.25)
            c = RegularPolygon(6).scale(0.32).set_stroke(WHITE, 2).shift(LEFT*0.8+DOWN*0.2)
            return VGroup(a, b, c)

        steps = [
            ("1 nm",                "≈10^-9 m",        1e-9,  ic_nm),
            ("Bacterium",           "≈10^-6 m",        1e-6,  ic_bact),
            ("Human",               "≈1 m",            1e0,   ic_human),
            ("Earth (diameter)",    "≈1.3×10^7 m",     1.3e7, ic_earth),
            ("Solar System",        "≈10^13 m",        1e13,  ic_solar),
            ("Oort Cloud",          "≈10^15 m",        1e15,  ic_oort),
            ("Nearby stars",        "≈10 ly ≈10^17 m", 1e17,  ic_stars),
        ]

        title = Text("Zoom ladder: feeling ×10^26", weight=BOLD).scale(0.8).to_edge(UP)
        subtitle = Text("Each step ~×10^3–×10^6 bigger", slant=ITALIC).scale(0.45).next_to(title, DOWN, buff=0.15)
        self.add(title, subtitle)

        # --- build cards ---
        cards = VGroup()
        for name, size_txt, _m, factory in steps:
            icon = factory()
            icon.set_height(CARD_ICON_H)
            cap = VGroup(
                Text(name).scale(0.45),
                Text(size_txt).scale(0.40).set_color(GREY_B),
            ).arrange(DOWN, buff=0.05)
            cards.add(VGroup(icon, cap).arrange(DOWN, buff=0.22))

        cards.arrange(RIGHT, buff=CARD_SPACING).to_edge(DOWN, buff=1.1)

        # --- continuous track behind ALL cards ---
        track_w = cards.get_width() + 2.0
        track = Rectangle(width=track_w, height=TRACK_H, fill_opacity=0.35,
                          fill_color=BLUE_E, stroke_width=0)
        track.move_to(cards.get_bottom()+UP*(TRACK_H/2+0.35))
        self.add(track, cards)

        # factor tag helper (no zoom glow)
        def show_factor(prev_m, next_m, near_mob):
            r = next_m / prev_m
            k = int(round(math.log10(r)))
            tag = MarkupText(f"×10<sup>{k}</sup>").scale(0.75).set_color(ACCENT)
            tag.next_to(near_mob, UP, buff=0.25)
            return Succession(FadeIn(tag, shift=UP*0.15, run_time=0.4),
                              FadeOut(tag, shift=UP*0.15, run_time=0.3))

        # --- camera: PAN ONLY (fixed width) ---
        self.camera.frame.set_width(CAMERA_WIDTH)
        self.play(self.camera.frame.animate.move_to(cards[0]), run_time=0.7, rate_func=smooth)

        for i in range(len(steps)-1):
            prev_m = steps[i][2]
            next_m = steps[i+1][2]
            next_card = cards[i+1]
            self.play(self.camera.frame.animate.move_to(next_card), run_time=0.7, rate_func=smooth)
            self.play(show_factor(prev_m, next_m, next_card))

        # overall callout (nm -> ~10 ly ≈ ×10^26)
        overall = VGroup(
            Text("Overall leap (example):", weight=MEDIUM).scale(0.55),
            MarkupText("1 nm → ~10 ly ≈ ×10<sup>26</sup>").scale(0.7).set_color(ACCENT),
        ).arrange(DOWN, buff=0.12).to_corner(UR, buff=0.6)
        self.play(FadeIn(overall, shift=UP*0.2), run_time=0.6)
        self.wait(0.6)
