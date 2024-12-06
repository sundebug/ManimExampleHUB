#  Copyright (c) 2024.  SunDebug
#  This file is a part of [Demo], based on [manimgl] by [3b1b]//
#  Created at : 2024-12-06 07:47
#  FileName   : "圆周角性质.py" modified at 2024-06 07:47:58
import numpy as np
from manimlib import *


class Angle(Arc):
    def __init__(self, start, end, point_o, **kwargs):
        self.start = start
        self.end = end
        self.point_o = point_o
        start_angle: float = (0,)
        angle: float = (TAU / 4,)
        radius: float = (1.0,)
        n_components: int = (8,)
        arc_center: Vect3 = (ORIGIN,)
        super().__init__(angle_center=point_o, **kwargs)


class CircleAngle(Scene):
    def construct(self):
        o = (-3, 0, 0)
        circle = Circle(radius=3, start_angle=PI / 4, arc_center=o, stroke_color=GREY_D)
        p, a, b, d = [
            circle.point_at_angle(angle * PI) for angle in (0.25, -0.3, 1.1, 1.25)
        ]
        P = Dot(p, fill_color=RED_D)
        O, A, B, D = [Dot(p) for p in (o, a, b, d)]
        label_O = Text("O").next_to(O, UP)
        label_P = Text("P").next_to(P, UP)
        label_A = Text("A").next_to(A, RIGHT)
        label_B = Text("B").next_to(B, LEFT)
        label_D = Text("D").next_to(D, DOWN)
        l_AB = Line(A, B)
        l_OA = Line(O, A)
        l_OB = Line(O, B)
        l_OP = DashedLine(P, D)
        l_AP = always_redraw(lambda: Line(A, P))
        l_BP = always_redraw(lambda: Line(B, P))
        texs = Tex(
            R"\angle{APB} = 65.0 \,\, ^\circ \angle{AOB}=135.0^\circ",
            t2c={'65': RED_D, r'\circ': BLUE_D, '135': RED_D},
        ).align_on_border(UL)

        tex_proof = Tex(
            R"&在圆中: \quad  \angle{OPB}=\angle{OBP} \\\ & \quad \quad \quad \quad \quad \angle{OPA}=\angle{OAP}\\\ "
            R"   \\\ &由外角性质:\quad \; \angle{BOD}=2 \times \angle{BPO}\\\ "
            R"&\qquad \qquad  \qquad  \quad \angle{BOD}=2 \times \angle{BPO}\\\ "
            R"\\\ & \angle{AOB}=2\times \angle{APB}",
            font_size=32,
            t2c={R"\angle{AOB}=2\times \angle{APB}": RED},
        ).align_on_border(RIGHT)
        angleAPB: DecimalNumber = texs.make_number_changeable(65.0)
        texs.make_number_changeable(135.0).set_value(
            angle_between_vectors(a - o, b - o) * 180 / PI
        )
        f_always(
            angleAPB.set_value,
            lambda: angle_between_vectors(a - P.get_center(), b - P.get_center())
            * 180
            / PI,
        )
        self.add(circle, O, P, A, B)
        self.add(l_AB, l_AP, l_BP, l_OA, l_OB)
        self.add(label_O, label_P, label_A, label_B)
        self.add(texs)

        self.play(
            MoveAlongPath(P, circle, rate_func=linear),
            MaintainPositionRelativeTo(label_P, P),
            run_time=10,
        )
        self.add(D, label_D)
        self.play(ShowCreation(l_OP))
        self.play(Write(tex_proof))
        self.wait(5)


if __name__ == '__main__':
    from RunScene import runScene

    runScene(CircleAngle)
