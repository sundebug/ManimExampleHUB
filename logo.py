from datetime import datetime

from manimlib import *

NEW_BLUE = "#68a8e1"


class Logo(Scene):
    __version__ = "0.1"
    __date__ = datetime.strptime("2024-07-08 14:51:00", "%Y-%m-%d %H:%M:%S")

    def construct(self) -> None:
        def get_x_axis(vt: ValueTracker):
            return ax.c2p(vt.get_value())

        def get_point_in_curve(vt: ValueTracker, gp: ParametricCurve):
            return gp.get_point_from_function(vt.get_value())

        def get_y_axis(vt: ValueTracker):
            return ax.c2p(0, fun_c(vt.get_value()))

        def fun_c(x: float):
            return 0.1 * (x + 3 - 5) * (x - 3 - 5) * (x - 5) + 4

        v_1 = ValueTracker(1.0)
        v_2 = ValueTracker(2.0)
        ax = (
            Axes(height=5, width=7, x_range=(-1, 10), y_range=(-1, 8))
            .next_to(LEFT_SIDE, RIGHT)
            .shift(UP * 1 + RIGHT * 0.2)
        )
        ax_labels = ax.get_axis_labels()

        graph = ax.get_graph(fun_c, x_range=(0.5, 9))
        v1x = SmallDot(get_x_axis(v_1))
        v1 = SmallDot(get_point_in_curve(v_1, graph))
        v1y = SmallDot(get_y_axis(v_1))
        v2x = SmallDot(get_x_axis(v_2))
        v2 = SmallDot(get_point_in_curve(v_2, graph))
        v2y = SmallDot(get_y_axis(v_2))
        v3 = SmallDot(ax.c2p(v_2.get_value(), fun_c(v_1.get_value())))
        dlv1 = ax.get_v_line_to_graph(v_1.get_value(), graph)
        dlv2 = ax.get_v_line_to_graph(v_2.get_value(), graph)
        dl_hv1 = ax.get_h_line_to_graph(v_1.get_value(), graph)
        dl_hv2 = ax.get_h_line_to_graph(v_2.get_value(), graph)
        dl1 = (
            Line(
                start=get_point_in_curve(v_1, graph),
                end=get_point_in_curve(v_2, graph),
                stroke_width=2,
            )
            .set_color(GREEN_D)
            .scale(2)
        )

        tri_kwargs = {
            "fill_color": WHITE,
            "fill_opacity": 1,
            "stroke_width": 0,
            "radius": 0.05,
        }
        tri_v1x, tri_v2x = [
            Triangle(**tri_kwargs).next_to(v, DOWN, buff=SMALL_BUFF) for v in [v1x, v2x]
        ]
        tri_v1y, tri_v2y = [
            Triangle(**tri_kwargs, start_angle=0).next_to(v, LEFT, buff=SMALL_BUFF)
            for v in [v1y, v2y]
        ]
        t_v1x = Tex(r"a", font_size=32).next_to(
            tri_v1x, direction=DOWN, buff=SMALL_BUFF
        )
        t_v2x = Tex(r"b", font_size=32).next_to(
            tri_v2x, direction=DOWN, buff=SMALL_BUFF
        )
        t_v1y = Tex(r"f(a)", font_size=32).next_to(
            tri_v1y, direction=LEFT, buff=SMALL_BUFF
        )
        t_v2y = Tex(r"f(b)", font_size=32).next_to(
            tri_v2y, direction=LEFT, buff=SMALL_BUFF
        )
        self.add(
            ax,
            ax_labels,
            graph,
            t_v1x,
            t_v2x,
            t_v1y,
            t_v2y,
            tri_v1x,
            tri_v1y,
            tri_v2x,
            tri_v2y,
        )
        self.add(
            dl_hv1,
            dl_hv2,
            dlv1,
            dlv2,
            dl1,
            v1,
            v2,
            pl := Polygon(
                v1.get_center(),
                v3.get_center(),
                v2.get_center(),
                v1.get_center(),
                stroke_width=2,
                stroke_color=RED_D,
                fill_color=RED_D,
                fill_opacity=1,
            ),
            TexText(r"$tan \theta$", font_size=16).next_to(pl, DOWN, buff=SMALL_BUFF),
        )
        self.play(GrowFromPoint(pl, pl.get_edge_center(DOWN)))

        def riemann_rect(s1: float, s2: float, n: int = None) -> Group:
            """
            函数下矩形
             :param s1: 端点1
             :param s2: 端点2
             :param n: 矩形个数
             :return:  Rectangle_group
            """

            if n is None:
                n = round(s2 - s1)
            delta = (s2 - s1) / n
            height_list = [
                graph.get_point_from_function(t)
                for t in [s1 + i * delta for i in range(n)]
            ]
            width = (ax.c2p(s2) - ax.c2p(s1)) / n
            base_h = ax.c2p(0)[1]
            group_Rect = (
                Group(
                    *[
                        Rectangle(
                            width=width[0],
                            height=p[1] - base_h,
                            fill_opacity=0.5,
                            stroke_width=0,
                            color=MANIM_COLORS[(i % 32) + 18],
                        )
                        for i, p in enumerate(height_list)
                    ]
                )
                .arrange_in_grid(n_cols=n, buff=0, aligned_edge=DOWN)
                .move_to(ax.c2p(s1), aligned_edge=DL)
            )
            return group_Rect

        self.play(FadeIn(riemann_rect(3, 9, 10)), lag_ratio=1)
        manim_name = TexText(r"Manim \\ \LaTeX").set_height(3).next_to(ax, RIGHT)
        manim_name[5:10].set_color(BLUE_D)

        manim_text = (
            Text("Mathematical Animation Engine", color=GREEN_D)
            .set_height(0.7)
            .next_to(ORIGIN, DOWN)
            .shift(DOWN * 2)
        )
        self.play(Write(manim_name))
        self.add(manim_text)
        self.play(FlashUnder(manim_text, color=GREEN_D))


if __name__ == "__main__":
    from RunScene import runScene

    runScene(Logo)
    log.info(f"{Logo.__date__.__str__()=}\n{Logo.__version__=}")
