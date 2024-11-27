# 成像公式  1/u+1/v = 1/f
import numpy as np
from manimlib import *
from manimlib import SceneState
from sympy.categories import Object

from RunScene import runScene


def cal_w_x(f, u, h=1):
    v = 0
    if f == -u:
        v = 7.5
        scale_factor = 3
    else:
        try:
            v = 1 / ((1 / f) + (1 / u))

        except ZeroDivisionError as e:
            print(e)
            v = 0
        finally:
            scale_factor = h * v / u
    return v, scale_factor


def generate_NumberLine(sc: Scene, f: float):
    focus_label = np.array((-2, -1, 0, 1, 2)) * f
    nl = NumberLine(include_ticks=False)
    sc.add(nl)
    for label, n in zip(["-2 f", "- f", "0", " f", "2 f"], focus_label):
        sc.add(
            Text(label, font_size=32, t2c={"f": RED_D}).next_to(nl.n2p(n), DOWN),
            nl.get_tick(n),
        )


class Convex:
    def __init__(self, len_center=0, len_height=2, len_focus=2):
        self.len_center = len_center
        self.len_height = len_height
        self.len_focus = len_focus
        self.cal = cal_w_x
        self.convex_len = VGroup(
            ArcBetweenPoints(
                np.array((self.len_center, self.len_height / 2, 0)),
                np.array((self.len_center, -self.len_height / 2, 0)),
                angle=PI / 3,
            ),
            ArcBetweenPoints(
                np.array((self.len_center, -self.len_height / 2, 0)),
                np.array((self.len_center, self.len_height / 2, 0)),
                angle=PI / 3,
            ),
        ).set_color(RED_D, opacity=0.3)

    def get_convex(self) -> VGroup:
        return self.convex_len

    def get_focus(self):
        return self.len_focus

    def get_c(self):
        return self.len_center


class Object_len(Arrow):
    def __init__(self, u, h, **kwargs):
        self.u = u
        self.h = h
        self.start = (u, 0, 0)
        self.end = (u, h, 0)
        super().__init__(start=self.start, end=self.end, buff=0, **kwargs)

    def get_u(self):
        self.u = self.get_start()[0]
        return self.u

    def get_h(self):
        return self.h


class Image_len(Arrow):
    def __init__(self, uo: Object_len, cv: Convex, **kwargs):
        self.v, self.h = cv.cal(cv.get_focus(), uo.get_u(), uo.get_h())
        self.start = np.array((self.v, 0, 0))
        self.end = np.array((self.v, self.h, 0))
        super().__init__(
            start=self.start,
            end=self.end,
            buff=0,
            fill_color=YELLOW_D,
            fill_opacity=0.3,
            **kwargs,
        )
        if self.v > 0:
            self.set_color(YELLOW_D, opacity=1)

    def get_v(self):
        self.v = self.get_start()[0]
        return self.v


def generateText(text1: Text, u_object: Object_len, v_object: Object_len, c_len):
    u_value = always_redraw(
        lambda: DecimalNumber().set_value(abs(u_object.get_u())).next_to(text1, RIGHT)
    )
    text2 = Text("像距:").next_to(u_value, RIGHT)
    v_value = always_redraw(
        lambda: DecimalNumber().set_value(abs(v_object.get_v())).next_to(text2, RIGHT)
    )
    text3 = Text(f"焦距{c_len.get_focus()}").next_to(v_value, RIGHT)

    text4 = Tex(r"\frac{1}{f}=\frac{1}{u}+\frac{1}{v}").align_on_border(UP)
    return text1, text2, text3, text4, u_value, v_value


class Concave:
    def __init__(self, len_center=0, len_height=2, len_focus=-2):
        self.len_center = len_center
        self.len_height = len_height
        self.len_focus = len_focus
        self.cal = cal_w_x
        self.concave_len = Polygon(
            *ArcBetweenPoints(
                np.array((self.len_center, self.len_height / 2, 0)),
                np.array((self.len_center, -self.len_height / 2, 0)),
                angle=PI / 3,
            )
            .shift(RIGHT / 3)
            .get_all_points(),
            *ArcBetweenPoints(
                np.array((self.len_center, -self.len_height / 2, 0)),
                np.array((self.len_center, self.len_height / 2, 0)),
                angle=PI / 3,
            )
            .shift(LEFT / 3)
            .get_all_points(),
            fill_opacity=0.3,
            fill_color=RED_D,
            stroke_opacity=1,
            stroke_color=RED_D,
        )

    def get_concave(self) -> VGroup:
        return self.concave_len

    def get_focus(self):
        return self.len_focus

    def get_c(self):
        return self.len_center

    def get_h(self):
        return self.len_height


class convex_len(Scene):
    state: SceneState
    u_object: Object_len

    def construct(self):
        f = 1.5
        u = -4
        h = 1
        generate_NumberLine(self, f)
        c_len = Convex(len_center=0, len_height=2, len_focus=f)
        u_object = Object_len(u, h)
        self.u_object = u_object
        v_object: Image_len = always_redraw(lambda: Image_len(u_object, c_len))
        text1 = Text("物距:").align_on_border(DL)

        def generate_light():
            # 通过光心的光线
            l1 = Polyline(
                u_object.get_top(),
                [c_len.get_c(), 0, 0],
                -4 * u_object.get_top(),
                color=GREEN,
            )
            # 平行光
            l2 = Polyline(
                u_object.get_top(),
                [c_len.get_c(), u_object.get_h(), 0],
                [c_len.get_focus(), 0, 0],
                [5 * c_len.get_focus(), -4 * u_object.get_h(), 0],
                color=PINK,
            )
            # 虚线光心光
            l3 = DashedLine(
                u_object.get_top(),
                [5 * u_object.get_u(), 5 * u_object.get_h(), 0],
                dash_length=0.25,
                color=GREEN,
            )
            # 虚线平行光
            l4 = DashedLine(
                [c_len.get_c(), u_object.get_h(), 0],
                [-5 * c_len.get_focus(), 6 * u_object.get_h(), 0],
                dash_length=0.25,
                color=PINK,
            )

            if u_object.get_u() > -c_len.get_focus():
                return VGroup(l1, l2, l3, l4)
            else:

                return VGroup(l1, l2)

        light = always_redraw(generate_light)

        self.add(*generateText(text1, u_object, v_object, c_len))
        self.add(c_len.get_convex().set_fill(RED_D, opacity=0.2), light)
        self.add(u_object, v_object)
        self.state = self.get_state()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        print(symbol)
        if symbol == 32:
            self.play(
                self.u_object.animate.shift(RIGHT * 3), run_time=5, rate_func=linear
            )
        else:
            self.restore_state(self.state)


class concave_len(Scene):
    def construct(self):
        f = -1.5
        u = -5
        h = 1

        generate_NumberLine(self, f)
        u_object = Object_len(u, h)
        c_len = Concave(len_center=0, len_height=2, len_focus=f)
        v_object: Image_len = always_redraw(lambda: Image_len(u_object, c_len))
        light_core = always_redraw(
            lambda: Polyline(
                u_object.get_top(), (c_len.get_c(), 0, 0), -u_object.get_top()
            ).set_color(GREEN_D)
        )
        light_para = always_redraw(
            lambda: VGroup(
                Polyline(
                    u_object.get_top(),
                    (c_len.get_c(), c_len.get_h() / 2, 0),
                    [-2 * c_len.get_focus(), 3 * c_len.get_h() / 2, 0],
                ),
                DashedLine(
                    [c_len.get_focus(), 0, 0],
                    [0, c_len.get_h() / 2, 0],
                    dash_length=0.2,
                ),
            ).set_color(PINK)
        )
        self.add(u_object, c_len.get_concave(), light_core, light_para, v_object)

        text1 = Text("凹透镜   物距:", text2color={"凹透镜": RED_D}).align_on_border(DL)
        self.add(*generateText(text1, u_object, v_object, c_len))
        self.play(u_object.animate.shift(RIGHT * 4), run_time=5, rate_func=linear)


if __name__ == "__main__":
    runScene(convex_len)
