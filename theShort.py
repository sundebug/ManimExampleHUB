from manimlib import *
from RunScene import runScene


class TheShort(Scene):
    def construct(self):
        l1 = Line(LEFT_SIDE, end=RIGHT_SIDE)
        p1 = Dot((-3, 3, 0))
        p2 = Dot((4, 2, 0))
        p3 = Dot(p2.get_center() * (1, -1, 0))
        p4 = Dot((0, 0, 0))
        route = always_redraw(
            lambda: VGroup(
                Line(p1.get_center(), p4.get_center(), color=GREEN_D),
                DashedLine(
                    p4.get_center(), p3.get_center(), color=YELLOW_D, dash_length=0.4
                ),
                Line(p4.get_center(), p2.get_center(), color=YELLOW_D),
            )
        )
        l2 = Line(p1.get_center(), p3.get_center()).set_color(RED_D)
        Ta = Text("K").next_to(p4, DOWN)
        for t, p in zip(["A", "B", "C"], [p1, p2, p3]):
            self.add(Text(t).next_to(p, DOWN))

        self.add(l1, l2, p1, p2, p3, p4, route, Ta)
        self.add(
            Text(
                "将军饮马:KA+KB=KA+KC>AC", font="SimHei", t2c={"将军饮马": RED_D}
            ).align_on_border(DOWN)
        )
        self.play(
            MoveAlongPath(p4, l1.copy().scale(0.9)),
            MaintainPositionRelativeTo(Ta, p4),
            run_time=10,
        )


if __name__ == "__main__":
    runScene(TheShort)
