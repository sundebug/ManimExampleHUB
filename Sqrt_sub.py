from manimlib import *

NEW_BLUE = "#68a8e1"


class D_math(Scene):  # 正弦曲线的切线
    def construct(self) -> None:

        ax = Axes(x_range=(-7, 7))

        pa = ValueTracker(1)
        graph: ParametricCurve = ax.get_graph(
            lambda x: np.sqrt(x + 2.2 * PI) - np.sin(x + PI) - 2, [-2 * PI, 2 * PI]
        )
        graph.set_stroke(width=1, color=PURPLE_D)

        point_1 = SmallDot(ax.c2p(pa.get_value(), 0))

        v_line = always_redraw(ax.get_v_line, point_1.get_center())
        h_line = always_redraw(ax.get_h_line, point_1.get_center())
        line: Line = ax.get_tangent_line(
            ax.get_x_axis().p2n(point_1.get_center()), graph
        )
        line.add_updater(
            lambda m: m.become(
                ax.get_tangent_line(ax.get_x_axis().p2n(point_1.get_center()), graph)
                .set_color(YELLOW_D)
                .set_stroke(width=1)
            )
        )

        self.add(ax, v_line, h_line, graph, line)
        tip_group = self.get_group(
            *[
                Vector(v, stroke_width=2, stroke_color=RED)
                for v in compass_directions(n=3)
            ]
        )
        tri_sign = ArrowTip()
        tri_sign_up = ArrowTip(angle=3 * PI / 2, width=0.2, length=0.2).next_to(
            point_1, UP, buff=0
        )
        tri_sign_down = ArrowTip(angle=PI / 2, width=0.2, length=0.2).next_to(
            point_1, DOWN, buff=0
        )

        def next_to_point(m: ArrowTip):
            if point_1.get_center()[1] > 0:
                m.become(tri_sign_up)
                m.next_to(point_1, UP, buff=0)
            else:
                m.become(tri_sign_down)
                m.next_to(point_1, DOWN, buff=0)

        tri_sign.add_updater(next_to_point)
        self.add(tri_sign)
        self.add()
        log.info(Vector().get_center())
        self.play(
            MoveAlongPath(point_1, graph.copy()),
            Rotating(tip_group, about_point=ax.c2p(2, 0)),
            run_time=30,
            lag_ratio=0,
        )
        point_1.add_updater(lambda p: self.bring_to_front(p))


class TEST(Scene):
    def construct(self) -> None:
        def graph_fun(x):
            return np.sin(x - 2 * PI) - 0.1 * x * x + 2

        ax = Axes(
            x_range=(-7, 7),
            x_axis_config={
                "include_ticks": True,
            },
        )
        graph = ax.get_graph(graph_fun, x_range=(-2 * PI, 2 * PI))
        graph.set_stroke(width=1, color=PURPLE_D)

        point_A = SmallDot(ax.c2p(0, 0))
        point_B = SmallDot(ax.c2p(PI + 0.2, 0))

        tri_A, tri_B = [
            Triangle(radius=0.1, stroke_width=0, fill_opacity=1).next_to(
                point, DOWN, buff=0
            )
            for point in [point_A, point_B]
        ]
        tri_A.set_color(YELLOW_D)
        tri_B.set_color(GREEN_D)

        v_line_A, v_line_B = [
            ax.get_v_line_to_graph(point.get_center()[0], graph)
            for point in [point_A, point_B]
        ]

        def update_v_line(m: Mobject, x: float, color):
            m.become(ax.get_v_line_to_graph(x, graph)).set_color(color)

        v_line_A.add_updater(
            lambda m: update_v_line(m, point_A.get_center()[0], GREEN_D)
        )
        v_line_B.add_updater(
            lambda m: update_v_line(m, point_B.get_center()[0], YELLOW_D)
        )

        line_graph = DashedLine(
            graph.get_point_from_function(point_A.get_center()[0]),
            graph.get_point_from_function(point_B.get_center()[0]),
        )

        def line_update(m: Mobject):
            m.become(
                DashedLine(
                    graph.get_point_from_function(point_A.get_center()[0]),
                    graph.get_point_from_function(point_B.get_center()[0]),
                )
                .set_stroke(width=1, color=YELLOW_D)
                .scale(1.5)
            )

        line_graph.add_updater(line_update)
        always(tri_A.next_to, point_A, DOWN, buff=0)
        always(tri_B.next_to, point_B, DOWN, buff=0)

        self.add(
            ax,
            point_A,
            tri_A,
            point_B,
            tri_B,
            graph,
            v_line_A,
            v_line_B,
            line_graph,
            ax.get_graph_label(graph, r"f(x)=\sin(x)", 1),
        )

        self.play(
            AnimationGroup(
                point_A.animate.shift(RIGHT * 1 * PI),
                point_B.animate.shift(LEFT * 1 * PI),
                run_time=3,
                lag_ratio=1,
            )
        )

        mG = Group()

        for m_obj in self.get_mobjects()[1:]:
            log.info(f"{m_obj = }")
            mG.add(m_obj)
        self.play(mG.animate.scale(0.5))


class Sqrt(Scene):  # 平方差公式
    """
    平方差公式
    还可以调整细节

    """

    def construct(self) -> None:
        sa = Square(side_length=3, fill_opacity=1, fill_color=GREEN_D)
        side_a = Tex("a^2").next_to(sa, DL, buff=-2.5)
        sb = Square(side_length=2, fill_opacity=1, fill_color=BLUE_D).align_to(sa, DL)
        side_b = Tex("b^2").next_to(sb, DL, buff=-1)
        ra = Rectangle(3, 1, fill_color=GREEN_D, fill_opacity=1).align_to(
            sa, direction=UL
        )
        rb = Rectangle(1, 2, fill_color=GREEN_D, fill_opacity=1).align_to(
            sa, direction=DR
        )

        self.add(sa, side_a)
        self.play(FadeIn(sb), FadeIn(side_b))
        self.add(ra, rb)
        self.play(Group(sa, sb, side_a, side_b).animate.to_edge(LEFT))
        self.play(Rotating(rb, TAU / 4, about_point=(1, 1, 0)), run_time=1)
        side_ra = Tex(r"a-b").next_to(rb, RIGHT)
        side_rb = Tex(r"a+b").next_to(Group(ra, rb), UP)
        self.play(FadeIn(Group(side_ra, side_rb)))
        ft = TexText(
            r"$a^2-b^2=(a+b)(a-b)$", font_size=128, t2c={"a": YELLOW_D, "b": RED_D}
        ).align_on_border(DOWN)
        ft[0].set_color(GREEN_D)
        aG = (
            Transform(side_a.copy(), ft[0:2]),  # a^2
            Transform(side_b.copy(), ft[3:5]),  # b^^2
            Transform(side_rb.copy(), ft[7:10]),  # a+b
            Transform(side_ra.copy(), ft[12:15]),  # a-b
        )
        self.play(aG[0])
        self.add(ft[2])  # -号
        self.play(aG[1])
        self.add(*[ft[x] for x in [5, 6, 10, 11, 15]])  # =号
        self.play(*[aG[2], aG[3]])


if __name__ == "__main__":
    from RunScene import runScene
    runScene(Sqrt)
