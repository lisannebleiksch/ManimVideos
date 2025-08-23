from manim import *

class ExpandingGrid(Scene):
    def construct(self):
        # Background
        self.camera.background_color = "#0c1736"
        
        # Create grid
        grid = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            axis_config={"stroke_color": GREY_B, "stroke_width": 1},
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1}
        )
        self.add(grid)

        # Animate expansion
        self.play(
            grid.animate.scale(3),  # expand the grid
            run_time=6,
            rate_func=there_and_back  # expands out, then contracts back
        )
        
        # Add glowing dots that drift apart
        dots = VGroup(*[Dot(point, color=YELLOW, radius=0.06) 
                        for point in [LEFT*2+UP*2, RIGHT*2+UP*1, DOWN*2, LEFT*3]])
        self.add(dots)

        self.play(
            *[dot.animate.shift(dot.get_center()*0.8) for dot in dots],
            run_time=5,
            rate_func=rate_functions.ease_in_out_sine
        )

        self.wait(2)
