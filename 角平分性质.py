#  Copyright (c) 2024.  SunDebug
#  This file is a part of [Demo], based on [manimgl] by [3b1b]
#  Created at : 2024-12-18 13:56
#  FileName   : "角平分性质.py" modified at 2024-18 13:56:56

from manimlib import *
from RunScene import Angle, generate_label


class Angle_bisector(Scene):
    def construct(self):
        title = (
            Tex(R"角平分线的性质")
            .set_color_by_gradient(PINK, TEAL_C)
            .align_on_border(UP)
        )
        v0, v1, v2 = points = vectors = np.asarray(
            [[-6, -1, 0], [-3, 3, 0], [-1, -1, 0]]
        )
        v3 = (v1 + v2) * 0.5
        vt = ValueTracker(0.35)

        lines = [Line(start=v0, end=v1), Line(start=v0, end=v2), Line(start=v0, end=v3)]
        angles = [
            Angle(v1, v3, v0, radius=0.5),
            Angle(v3, v2, v0, radius=0.5).set_color(RED_C),
        ]
        labels = generate_label(3, points)
        point_p = always_redraw(
            lambda: Dot(
                lines[2].get_start() + vt.get_value() * lines[2].get_vector(),
                fill_color=RED_C,
            )
        )
        lines_ab = always_redraw(
            lambda: VGroup(
                *[
                    DashedLine(p, n.get_projection(p))
                    for p, n in zip([point_p.get_center() for _ in range(2)], lines[:2])
                ]
            )
        )
        label_p, label_h1, label_h2 = labels_ab = [
            Tex("P", font_size=32).next_to(point_p, UR),
            Tex("h_1", font_size=32).next_to(lines_ab[0].get_center(), DL),
            Tex("h_2", font_size=32).next_to(lines_ab[1].get_center(), LEFT),
        ]
        ag = AnimationGroup(
            MaintainPositionRelativeTo(label_p, point_p),
            MaintainPositionRelativeTo(label_h1, lines_ab[0]),
            MaintainPositionRelativeTo(label_h2, lines_ab[1]),
        )
        proof_tex = Tex(
            R"""
            \angle{CAP} &= \angle{BAP} \\
            &\Updownarrow \\
            h_1 &= h_2
        """,
            font_size=48,
            t2c={R"\Updownarrow": RED},
        ).align_on_border(RIGHT)

        self.add(
            title, *lines, *angles, *labels, lines_ab, point_p, *labels_ab, proof_tex
        )
        self.play(vt.animate.set_value(1), ag, run_time=10)
        self.wait(5)


if __name__ == '__main__':
    from RunScene import runScene

    runScene(Angle_bisector)
