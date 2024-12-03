from yaml import safe_load
from manimlib import Scene, SceneFileWriter, Mobject, Tex, log
from manimlib.config import parse_cli, get_configuration, get_custom_config
from manimlib.extract_scene import get_scene_config
from manimlib.utils.dict_ops import merge_dicts_recursively
from typing import Sequence
from rich import print


def show_scene_config():
    args = parse_cli()
    config = get_configuration(args)

    custom_config = get_custom_config()
    scene_config = get_scene_config(config)
    # with open("scene_config.yaml", "w") as f:
    #     f.write(yaml.dump(scene_config, default_flow_style=False))

    return config, custom_config, scene_config


def runScene(scene: Scene.__class__, **kwargs) -> None:
    yaml_config = {}
    try:
        with open("scene_config.yaml") as f:
            yaml_config = safe_load(f)
    except FileNotFoundError as e:
        print("file not find", e)
    if log.level == log.DEBUG:
        print(f"debug mode, {yaml_config=},{kwargs=}")
    yaml_config = merge_dicts_recursively(yaml_config, kwargs)
    scene(**yaml_config).run()


# todo
def writeScene(scene: Scene.__class__) -> None:
    yaml_config = {}
    try:
        with open("scene_config.yaml") as f:
            yaml_config = safe_load(f)
    except FileNotFoundError as e:
        print("file not find", e)
    sc: Scene = scene(**yaml_config)
    sfw = SceneFileWriter(sc, **sc.file_writer_config)
    sfw.begin()
    print(sfw.get_movie_file_path())
    # sfw.open_movie_pipe("sc.mp4")
    # sfw.begin_animation()
    # sfw.write_frame(sc.camera)
    # sfw.close_movie_pipe()
    # sfw.finish()


def generate_label(
    labels: Sequence[str] | int,
    mobjs: Sequence[Mobject],
    directions: Sequence,
):
    if isinstance(labels, int):
        labels = [chr(i + 65) for i in range(labels)]
    return [Tex(t).next_to(p, v) for t, p, v in zip(labels, mobjs, directions)]
