import manimlib.utils.space_ops
import numpy as np
from manimlib import *
from RunScene import generate_label


class bisector_angle(Scene):
    def construct(self):
        angle = 24 * DEG
        A = np.asarray((0, 0, 0))
        B = np.asarray((4, 0, 0))
        D = rotate_vector(B, angle)
        temp = rotate_vector(B, angle * 2)
        C = find_intersection(temp, temp, B, D - B)
        lines = [Line(A, B), Line(A, C), Line(B, C), Line(A, D)]
        E, F = [lines[i].get_projection(D) for i in (0, 1)]
        G = lines[2].get_projection(A)
        dashed_lines = [
            DashedLine(D, E, dash_length=0.15, color=RED_D),
            DashedLine(D, F, dash_length=0.15, color=RED_D),
            DashedLine(A, G, dash_length=0.15, color=GREEN_D),
        ]
        dots = [Dot(p, fill_color=WHITE) for p in [A, B, C, D, E, F, G]]
        dot_labels = generate_label(
            7, [A, B, C, D, E, F, G], [DOWN, DOWN, UP, RIGHT, DOWN, UL, RIGHT]
        )
        triangles = VGroup(
            Polygon(A, B, D, fill_color=LIGHT_PINK, fill_opacity=0.3, stroke_opacity=0),
            Polygon(
                A, C, D, fill_color=LIGHT_BROWN, fill_opacity=0.3, stroke_opacity=0
            ),
        )
        vg = VGroup(
            *lines, *dashed_lines, *dots, *dot_labels, *triangles
        ).align_on_border(UL)
        texts = [
            r'\angle{BAD}=\angle{CAD} \Rightarrow \; DE=DF',
            r'S_{\triangle{BAD}}=AB \times DE =BD \times AG',
            r'S_{\triangle{CAD}}=AC \times DF = CD \times AG',
            r'\frac{S_{\triangle{BAD}}}{S_{\triangle{CAD}}}=\frac{AB}{AC}= \frac{BD}{CD}',
        ]
        tex_group = (
            VGroup(
                Tex(
                    texts[3],
                    t2c={
                        r"S_{\triangle{CAD}}": LIGHT_BROWN,
                        r"S_{\triangle{BAD}}": LIGHT_PINK,
                    },
                ),
                Tex(
                    texts[2],
                    t2c={
                        r"S_{\triangle{CAD}}": LIGHT_BROWN,
                        r"DF": RED_D,
                        r"AG": GREEN_D,
                    },
                ),
                Tex(
                    texts[1],
                    t2c={
                        r"S_{\triangle{BAD}}": LIGHT_PINK,
                        r"DE": RED_D,
                        r"AG": GREEN_D,
                    },
                ),
                Tex(texts[0]),
            )
            .arrange_to_fit_height(4, about_edge=BOTTOM)
            .align_on_border(RIGHT)
        )
        self.add(
            Tex(r"角平分线定理")
            .set_color_by_gradient(LIGHT_PINK, LIGHT_BROWN)
            .align_on_border(DOWN)
        )
        self.add(*lines, *dots, *dot_labels)
        self.play(ShowCreation(dashed_lines[2]))
        self.play(ShowCreation(dashed_lines[0]), ShowCreation(dashed_lines[1]))
        self.play(Write(tex_group[3]))
        self.play(ShowCreation(triangles[0]), Write(tex_group[2]), lag_ratio=0)

        self.play(ShowCreation(triangles[1]), Write(tex_group[1]), lag_ratio=0)
        self.play(Write(tex_group[0]))
        self.wait(5)


if __name__ == '__main__':
    from RunScene import runScene

    runScene(bisector_angle, preview=True)
