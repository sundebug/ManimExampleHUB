#  Copyright (c) 2024.  SunDebug
#  This file is a part of [Demo], based on [manimgl] by [3b1b]
#  Created at : 2024-12-17 15:02
#  FileName   : "抛物线.py" modified at 2024-17 15:02:12
from manimlib import *


class Parabola(Scene):

    arrow_config = dict(buff=0, thickness=2, tip_width_ratio=4, tip_angle=PI / 6)

    def construct(self):
        self.add(
            Tex(R"斜上抛物体的运动轨迹")
            .set_color_by_gradient(RED, BLUE_D)
            .align_on_border(UL)
            .shift(RIGHT)
        )

        def parabola_fun(x):
            return np.asarray([x, -((x / 2 - 2) ** 2) + 4])

        def d_parabola_fun(x, dx):
            return x + dx, dx * (-x / 2 + 2)

        t = ValueTracker()
        ax = NumberPlane(x_range=(0, 8), y_range=(0, 4.5)).align_on_border(DL, buff=1)
        ax.add_coordinate_labels(excluding=None)
        bullet = Dot(ax.get_origin(), fill_color=RED).add_updater(
            lambda m: m.move_to(ax.c2p(*parabola_fun(t.get_value())))
        )
        trace = TracedPath(lambda: bullet.get_center(), stroke_opacity=0.5)
        tail = TracingTail(
            lambda: bullet.get_center(), stroke_color=RED_D, stroke_width=5
        )

        v_0 = Vector((*d_parabola_fun(0, 0.5), 0), **Parabola.arrow_config).move_to(
            ax.get_origin(), aligned_edge=DL
        )
        self.add(*[m for m in locals().values() if isinstance(m, Mobject)])
        parabola_ani = AnimationGroup(
            t.animate.set_value(8), run_time=5, rate_func=linear
        )

        # 速度分解
        ax1 = Axes(x_range=(0, 2), y_range=(0, 2)).align_on_border(UR).shift(DOWN)
        v_1 = Vector((*d_parabola_fun(0, 0.8), 0), **Parabola.arrow_config).move_to(
            ax1.get_origin(), aligned_edge=DL
        )
        v_1_y = Vector(
            (0, d_parabola_fun(0, .8)[1], 0),
            **Parabola.arrow_config,
            fill_color=YELLOW_D
        ).move_to(ax1.get_origin(), aligned_edge=DOWN)
        v_1_x = Vector(
            (d_parabola_fun(0, .8)[0], 0, 0),
            **Parabola.arrow_config,
            fill_color=YELLOW_D
        ).move_to(ax1.get_origin(), aligned_edge=LEFT)
        ani_group = AnimationGroup(
            FadeIn(Tex(R"v_0").next_to(v_1, UR, buff=0.1)),
            FadeIn(
                Arc(
                    angle=v_1.get_angle(),
                    arc_center=v_1.get_start(),
                    radius=0.3,
                    stroke_width=1,
                )
            ),
            FadeIn(
                Tex(r"\theta", font_size=32, fill_color=RED).next_to(
                    ax1.get_origin(), UR, buff=0.25
                )
            ),
            TransformFromCopy(v_1, v_1_x),
            FadeIn(
                Tex(R"v_x=v_0 \cdot cos(\theta)", font_size=24).next_to(
                    v_1_x, DOWN, buff=0.1
                )
            ),
            TransformFromCopy(v_1, v_1_y),
            FadeIn(
                Tex(R"v_y=v_0 \cdot sin(\theta)", font_size=24).next_to(
                    v_1_y, LEFT, buff=0.1
                )
            ),
            run_time=2,
            lag_ratio=1,
        )
        ani_tex = AnimationGroup(
            Write(
                Tex(
                    R"t& =2 \times  \frac{v_y}{g}\\ h &= \frac{1}{2}v_y t = \frac{v_y^2}{g}  \\ s &= v_x \times t =2 \frac{v_x v_y}{g}\\ &g 为重力加速度",
                    font_size=28,
                )
                .align_on_border(RIGHT)
                .shift(DOWN * 2)
            )
        )

        self.play(parabola_ani)
        self.play(FadeInFromPoint(VGroup(ax1, v_1), ax.get_origin()))
        self.play(ani_group)
        self.play(ani_tex)


if __name__ == '__main__':
    from RunScene import runScene

    runScene(Parabola)
