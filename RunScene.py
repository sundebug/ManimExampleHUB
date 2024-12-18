from typing import Sequence, Callable
from manimlib import *

# todo

# 目前不用的
# def writeScene(scene: Callable) -> None: ...

# def runScene_new(scene: Callable, **kwargs) -> None:
#     print(f"ManimGL \033[32mv{__version__}\033[0m")
#     with open("scene_config.yaml", "r") as f:
#         scene_config = unsafe_load(f)
#         scene_config.update(window=Window(**scene_config.pop('window_config')))
#
#     scene(**scene_config).run()


class Angle(Arc):
    def __init__(self, v1, v2, v0, **kwargs):
        self.angle = angle_between_vectors(normalize(v2 - v0), normalize(v1 - v0))
        self.start_angle = min(
            abs(angle_of_vector(normalize(v2 - v0))),
            abs(angle_of_vector(normalize(v1 - v0))),
        )
        self.arc_center = v0
        self.center_v = normalize((v1 + v2) / 2 - v0)
        super().__init__(
            start_angle=self.start_angle,
            angle=self.angle,
            arc_center=self.arc_center,
            **kwargs,
        )

    def get_angle(self):
        return self.angle * 180 / np.pi

    def add_label(self, label, **kwargs):
        self.add(
            Tex(label, font_size=32).next_to(self.get_center(), direction=self.center_v)
        )
        return self


def generate_label(
    labels: Sequence[str] | int, mobjs: Sequence, directions=None, **kwargs
):
    import numpy as np
    from manimlib import Tex

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


def runScene(scene: Callable, **kwargs) -> None:
    from manimlib import Window, __version__
    from manimlib.config import manim_config
    from addict import Dict

    print(f"ManimGL \033[32mv{__version__}\033[0m")
    scene_config = Dict(manim_config.scene)
    window = Window(**manim_config.window)
    scene_config.update(window=window)
    scene(**scene_config).run()


def end_tip(func):
    def wrapper(*args, **kwargs):
        log.info(f"{func=}开始运行")
        func(*args, **kwargs)
        log.info(f"{func.__name__=}运行结束")
        return func(*args, **kwargs)

    return wrapper


if __name__ == '__main__':
    from addict import Dict
    from manimlib import log, __version__, Scene
    from manimlib.config import manim_config

    @end_tip
    class Test(Scene):
        def construct(self):
            from manimlib import Circle

            self.add(Circle())

    runScene(Test)
