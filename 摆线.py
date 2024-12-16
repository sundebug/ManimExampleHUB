#  Copyright (c) 2024.  SunDebug
#  This file is a part of [Demo], based on [manimgl] by [3b1b]
#  Created at : 2024-12-15 14:21
#  FileName   : "摆线.py" modified at 2024-15 14:21:35
from manimlib import *


class Cycloid(Scene):

    def construct(self):
        r = 1
        line = Line(LEFT_SIDE, RIGHT_SIDE).shift(DOWN * r)
        small_circle = Circle(radius=r, stroke_color=YELLOW, stroke_width=4).shift(
            LEFT * 6
        )
        dot = Dot(fill_color=RED).shift(LEFT * (6 - r) - (r, r, 0))
        l_r = Line(small_circle.get_center(), dot)
        label_r = Text("r").next_to(l_r, LEFT)

        def update_line(rg, dt):
            rg.shift(dt * r * RIGHT)
            rg.rotate(-dt, about_point=rg[0].get_center())

        rotate_group = VGroup(small_circle, dot, l_r, label_r).add_updater(update_line)
        path = TracedPath(dot.get_center, stroke_width=2, stroke_color=YELLOW_D)
        texes = (
            Tex(
                R"摆线:\left\{ \begin{aligned} & x=r(r-sin(t)) \\\\ &y= r(1-cos(t) \end{aligned} \right."
            )
            .set_color_by_gradient(YELLOW_D, RED_C)
            .align_on_border(UP)
        )

        self.add(rotate_group, path, line, l_r, label_r, texes)
        self.play(Write(texes), run_time=4)
        self.wait(10)


if __name__ == '__main__':
    from RunScene import runScene

    runScene(Cycloid)
