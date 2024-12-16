#  Copyright (c) 2024.  SunDebug
#  This file is a part of [Demo], based on [manimgl] by [3b1b]
#  Created at : 2024-12-16 10:56
#  FileName   : "摆线1.py" modified at 2024-16 10:56:42
import numpy as np
from manimlib import *


class Cycloid_1(Scene):
    def construct(self):
        texes = (
            Tex(
                R"摆线:\left\{ \begin{aligned} & x=r(t-sin(t)) \\\\ &y= r(1-cos(t) \end{aligned} \right.",
                font_size=32,
            )
            .set_color_by_gradient(YELLOW_D, RED_C)
            .align_on_border(UL)
        )
        self.add(texes)
        ax = Axes(x_range=(-1, 12.5), y_range=(-1, 2)).align_on_border(DOWN, 2)
        ax.add_coordinate_labels()

        vt = ValueTracker()
        func_graph = always_redraw(
            lambda: ax.get_parametric_curve(
                lambda t: (1 * (t - np.sin(t)), 1 * (1 - np.cos(t)), 0),
                t_range=(0, vt.get_value(), 0.1),
            )
        )
        texes1 = Tex(
            R"令r =1 \quad \quad t&=0.0 \\ x&=0.0 \\y& =0.0 ", font_size=32
        ).align_on_border(UP)
        t_value = texes1.make_number_changeable("0.0")
        x_value = texes1.make_number_changeable("0.0")
        y_value = texes1.make_number_changeable("0.0")
        t_value.add_updater(lambda t: t.set_value(vt.get_value()))
        x_value.add_updater(
            lambda t: t.set_value((vt.get_value() - np.sin(vt.get_value())))
        )
        y_value.add_updater(lambda t: t.set_value((1 - np.cos(vt.get_value()))))
        self.add(ax, func_graph, texes1)
        self.play(vt.animate.set_value(12),rate_func=linear, run_time=10)
        self.wait(10)


if __name__ == '__main__':
    from RunScene import runScene

    runScene(Cycloid_1)
