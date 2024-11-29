from manimlib import *


class TheShort(Scene):
    def construct(self):
        l1 = Line(LEFT_SIDE, end=RIGHT_SIDE)
        pa = Dot((-3, 3, 0))
        pb = Dot((4, 2, 0))
        pc = Dot(pb.get_center() * (1, -1, 0))
        pk = Dot((0, 0, 0))
        route = always_redraw(
            lambda: VGroup(
                Line(pa.get_center(), pk.get_center(), color=GREEN_D),
                DashedLine(
                    pk.get_center(), pc.get_center(), color=YELLOW_D, dash_length=0.4
                ),
                Line(pk.get_center(), pb.get_center(), color=YELLOW_D),
            )
        )
        l2 = Line(pa.get_center(), pc.get_center()).set_color(RED_D)
        Tk = Text("K").next_to(pk, DOWN)
        for t, p in zip(["A", "B", "C"], [pa, pb, pc]):
            self.add(Text(t).next_to(p, DOWN))

        self.add(l1, l2, pa, pb, pc, pk, route, Tk)
        tt = (
            VGroup(
                Tex(r"将军饮马:", font_size=48, tex_to_color_map={"将军饮马": RED}),
                Tex("KA+KB"),
                Tex("=KA+KC\ge"),
                Tex(r"AC ="),
            )
            .align_on_border(DOWN)
            .arrange_to_fit_width(9.5)
        )
        bb = Brace(tt[1], UP)
        Lac = DecimalNumber(
            Line(pc.get_center(), pa.get_center()).get_length(), color=RED
        ).next_to(tt[-1], RIGHT)
        Lakb = always_redraw(
            lambda: DecimalNumber(
                Line(pk.get_center(), pa.get_center()).get_length()
                + Line(pk.get_center(), pb.get_center()).get_length(),
                color=RED,
            ).next_to(bb, UP)
        )

        self.add(*tt, bb, Lac, Lakb)
        self.play(
            MoveAlongPath(pk, l1.copy().scale(0.9), rate_func=there_and_back),
            MaintainPositionRelativeTo(Tk, pk),
            run_time=10,
        )


if __name__ == "__main__":
    from RunScene import runScene

    runScene(TheShort)
