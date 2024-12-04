import numpy as np
from manimlib import *
from RunScene import generate_label


class Fermat(Scene):
    def construct(self):

        pl = Polygon((-2, -1, 0), (2, -1, 0), (1, 3, 0))
        A, B, C = pl.get_vertices()
        self.p = Dot(fill_color=RED_D)
        P = self.p.get_center()
        label_ABC = VGroup(*generate_label(3, pl.get_vertices(), (LEFT, RIGHT, UP)))
        tri_ACP = always_redraw(
            lambda: Polygon(A, C, P, fill_opacity=0.5, stroke_opacity=0)
        )
        tri_ACP_p: Polygon = always_redraw(
            lambda: Polygon(A, C, P, fill_opacity=0.5, stroke_opacity=0).rotate(
                PI / 3, about_point=A
            )
        )

        lines = VGroup(
            always_redraw(lambda: Line(P, A, color=YELLOW_D)),
            always_redraw(lambda: Line(P, B, color=GREEN_D)),
            always_redraw(lambda: Line(P, C, color=BLUE_D)),
        )
        dots = VGroup(*[Dot(v, fill_color=RED) for v in (A, B, C)])

        A1, C1, P1 = tri_ACP_p.get_vertices()
        AC1 = Line(A1, C1)
        PP1 = always_redraw(lambda: Line(P, P1, color=YELLOW_D))
        CP1 = always_redraw(lambda: Line(C1, P1, color=BLUE_D))
        AP1 = always_redraw(lambda: Line(A1, P1, color=YELLOW_D))
        CC1 = DashedLine(C, C1, dash_length=0.2)
        label_P = Text("P")
        f_always(label_P.next_to, lambda: P - 0.5)
        label_C1 = Tex(r"C'").next_to(tri_ACP_p.get_vertices()[1], LEFT)
        label_P1 = Tex(r"P'")
        f_always(label_P1.next_to, lambda: tri_ACP_p.get_vertices()[2], direction=UP)
        BC1 = DashedLine(C1, B, dash_length=0.2, color=PINK)
        tex_title = Tex(
            r"&\angle{PAP'} = \angle{CAC'} = 60^o \quad  \quad \triangle{ACP}\cong \triangle{AC'P'} \\&费马点: PB +PA "
            r"+PC = PB + PP' +P'C' \ge BC'",
        ).align_on_border(DOWN)

        self.add_mobjects_among(locals().values())

        self.play(MoveAlongPath(self.p, Circle(radius=0.5).shift(RIGHT)), run_time=5)
        self.wait(5)


if __name__ == '__main__':
    from RunScene import runScene

    runScene(Fermat)
