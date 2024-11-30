from manimlib import *


class DemoRotate(Scene):
    def construct(self):
        nplan = NumberPlane(
            axis_config={"stroke_color": BLUE_D},
            faded_line_style={
                "stroke_color": '#333',
                "stroke_width": 0.5,
                "stroke_opacity": 0,
            },
        )
        angle = 140 * DEGREES
        r_origin = (-1, -1, 0)
        A, B, C = [(1, 3, 0), (1, 1, 0), (4, 0.5, 0)]
        tri = Polygon(A, B, C, stroke_width=5, fill_color=GREY_D, fill_opacity=1)
        p = Dot(r_origin)
        DashedLineGroup = VGroup()
        for v in tri.get_vertices():
            DashedLineGroup.add(
                Line(
                    r_origin,
                    v,
                    color=GREY,
                )
            )
        DashedLineGroup_copy = DashedLineGroup.copy()
        aG = AnimationGroup(
            *[
                Rotating(m.set_color(GREEN_D), angle, about_point=r_origin)
                for m in DashedLineGroup_copy
            ],
            lag_ratio=1
        )
        arc = always_redraw(
            lambda: ArcBetweenPoints(
                start=C,
                end=DashedLineGroup_copy[-1].get_end(),
                angle=angle_between_vectors(C, DashedLineGroup_copy[-1].get_end()),
                arc_center=r_origin,
            ).scale(0.1, about_point=r_origin),
        )
        arc1 = always_redraw(
            lambda: ArcBetweenPoints(
                start=B,
                end=DashedLineGroup_copy[1].get_end(),
                angle=angle_between_vectors(B, DashedLineGroup_copy[1].get_end()),
                arc_center=r_origin,
                stroke_color=YELLOW,
            ).scale(0.3, about_point=r_origin),
        )
        labels_tri = VGroup(
            Tex(s).next_to(p, d)
            for s, p, d in zip(
                ["A", "B", "C"], tri.get_vertices(), [UP, LEFT, DOWN, RIGHT]
            )
        )

        self.add(DashedLineGroup, nplan, tri, p, arc, arc1, labels_tri)
        self.add(Tex("O").next_to(r_origin, DOWN))
        self.play(aG, run_time=2)
        tri_copy = Polygon(
            *[vex.get_end() for vex in DashedLineGroup_copy], stroke_width=5, color=PINK
        )
        labels_tri1 = VGroup(
            Tex(s).next_to(p, d)
            for s, p, d in zip(
                ["A'", "B'", "C'"], tri_copy.get_vertices(), [DOWN, RIGHT, UP]
            )
        )
        self.play(ShowCreation(tri_copy))
        self.add(labels_tri1)
        tri_copy.set_fill(PINK, opacity=0.5)
        self.play(
            FadeInFromPoint(
                Tex(r"图形绕定点旋转后,\\图形上的所有点都绕定点旋转同一角度")
                .align_on_border(DOWN + RIGHT)
                .set_color_by_gradient(BLUE_D, YELLOW),
                point=r_origin,
            )
        )


if __name__ == '__main__':
    from RunScene import runScene

    runScene(DemoRotate)
