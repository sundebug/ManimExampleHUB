from addict import Dict
from typing import Sequence, Callable

from glumpy.graphics.svg.shapes import Polygon
from yaml import unsafe_load, dump

from manimlib.config import manim_config
from manimlib import (
    Scene,
    Mobject,
    Window,
    Tex,
    RED_D,
    BLUE_D,
    RegularPolygon,
    ShowCreation,
)
import numpy as np
from manimlib import log, __version__


# todo
def writeScene(scene: Scene.__class__) -> None: ...


def generate_label(
    labels: Sequence[str] | int, mobjs: Sequence[Mobject], directions=None, **kwargs
):
    if directions is None:
        directions = []
    if isinstance(labels, int):

        labels = [
            chr(i + 65) for i in range(labels if labels < len(mobjs) else len(mobjs))
        ]
    if directions is None:
        directions = []
    if len(directions) < len(mobjs):
        directions = [
            *directions,
            *[np.array((0, -1, 0)) for _ in range(len(mobjs) - len(directions))],
        ]
    return [
        Tex(t, **kwargs).next_to(p, v) for t, p, v in zip(labels, mobjs, directions)
    ]


def runScene_new(scene: Scene.__class__, **kwargs) -> None:
    print(f"ManimGL \033[32mv{__version__}\033[0m")
    with open("scene_config.yaml", "r") as f:
        scene_config = unsafe_load(f)
        scene_config.update(window=Window(**scene_config.pop('window_config')))

    scene(**scene_config).run()


def runScene(scene: Callable, **kwargs) -> None:

    print(f"ManimGL \033[32mv{__version__}\033[0m")
    scene_config = Dict(manim_config.scene)
    window = Window(**manim_config.window)
    scene_config.update(window=window)
    scene(**scene_config).run()


def end_tip(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        log.info(f"{func.__name__=}运行结束")
        return func(*args, **kwargs)

    return wrapper


@end_tip
class Test(Scene):
    def construct(self):
        from manimlib import RegularPolygon, DOWN

        poly = RegularPolygon()
        labels = generate_label(["A", 'C', 'D', "K"], poly.get_vertices())

        self.play(Tex(R"\to 中k国").animate.shift((2, 0, 0)))
        self.play(ShowCreation(poly))
        self.add(*labels)


if __name__ == '__main__':
    runScene(Test, a=2)
