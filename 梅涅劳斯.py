#  Copyright (c) 2024.  SunDebug
#  This file is a part of [Demo], based on [manimgl] by [3b1b]
#  Created at : 2024-12-13 12:57
#  FileName   : "梅涅劳斯.py" modified at 2024-13 12:57:47
import numpy as np
from manimlib import *
from RunScene import generate_label


class menelaus(Scene):
    def construct(self):
        positions = np.asarray(((-4, 0, 0), (-3, 2, 0), (-1, 0, 0), (-5, 0, 0)))
        pa, pb, pc, pd = [SmallDot(p) for p in positions]

        tri_ABC = Polygon(*positions[:-1])
        k = ValueTracker(0.2)

        pf = always_redraw(
            lambda: SmallDot(
                (1 - k.get_value()) * positions[2] + positions[1] * k.get_value()
            )
        )
        pe = always_redraw(
            lambda: SmallDot(
                line_intersection(
                    (positions[-1], pf.get_center()), (positions[0], positions[1])
                )
            )
        )
        lines = [
            Line(pa, pc),
            always_redraw(lambda: Line(pc, pf, color=YELLOW_D)),
            always_redraw(lambda: Line(pf, pb, color=BLUE_D)),
            always_redraw(lambda: Line(pb, pe, color=YELLOW_D)),
            always_redraw(lambda: Line(pe, pa, color=BLUE_D)),
            always_redraw(lambda: Line(pa, pd, color=YELLOW_D)),
            always_redraw(lambda: Line(pd, pe)),
            always_redraw(lambda: Line(pe, pf)),
        ]
        tex_color_map = {
            "AD": YELLOW_D,
            "CF": YELLOW_D,
            "BE": YELLOW_D,
            "DC": BLUE_D,
            "FB": BLUE_D,
            "EA": BLUE_D,
            "1": RED_D,
        }
        title = Tex(R"梅涅劳斯定理:").align_on_border(UL)
        tex = Tex(
            R"\quad \frac{AD}{DC} \times\frac{CF}{FB} \times\frac{BE}{EA} =1",
            tex_to_color_map=tex_color_map,
        ).align_on_border(DOWN)
        pg = always_redraw(
            lambda: SmallDot(
                find_intersection(
                    pc.get_center(),
                    Line(pa, pb).get_vector(),
                    pd.get_center(),
                    Line(pd, pe).get_vector(),
                )
            )
        )
        labels = generate_label(
            7,
            [pa, pb, pc, pd, pe, pf, pg],
            [DOWN, UP, DOWN, DOWN, UP, DOWN, RIGHT],
            font_size=24,
        )
        l = always_redraw(lambda: DashedLine(pc, pg))
        ll = always_redraw(lambda: DashedLine(pf, pg))
        proof_tex = R'''
       &做CG\mathop{//}AB 交DF于G\\ \\
       &\frac{AD}{DC} = \frac{AE}{CG} \quad
       \frac{CF}{FB} = \frac{CG}{EB} \\ \\
       &\frac{AD}{DC} \times\frac{CF}{FB} \times\frac{BE}{EA} =  
       \frac{AE}{CG} \times \frac{CG}{EB} \times \frac{BE}{EA}= 1 
        '''
        tex1 = Tex(proof_tex, t2c=tex_color_map, font_size=24).align_on_border(UR)

        self.add(pa, pb, pc, pd, pe, pf, pg, *labels, *lines, title, tex, l, ll)
        self.play(
            k.animate.set_value(0.7),
            MaintainPositionRelativeTo(labels[5], pf),
            MaintainPositionRelativeTo(labels[4], pe),
            MaintainPositionRelativeTo(labels[6], pg),
            run_time=5,
        )
        self.play(
            k.animate.set_value(0.5),
            MaintainPositionRelativeTo(labels[5], pf),
            MaintainPositionRelativeTo(labels[4], pe),
            MaintainPositionRelativeTo(labels[6], pg),
            run_time=3,
        )
        self.wait()

        self.play(ShowCreation(tex1, run_time=5))
        self.wait(5)


if __name__ == '__main__':
    from RunScene import runScene

    runScene(menelaus)
