from yaml import safe_load
from manimlib import Scene
from manimlib import SceneFileWriter
from manimlib.config import parse_cli, get_configuration, get_custom_config
from manimlib.extract_scene import get_scene_config


def show_scene_config():
    args = parse_cli()
    config = get_configuration(args)
    get_custom_config()
    scene_config = get_scene_config(config)
    print(scene_config)
    # with open("scene_config.yaml", "w") as f:
    #     f.write(yaml.dump(scene_config, default_flow_style=False))

    return scene_config


def runScene(scene: Scene.__class__) -> None:
    yaml_config = {}
    try:
        with open("scene_config.yaml") as f:
            yaml_config = safe_load(f)
    except FileNotFoundError as e:
        print("file not find", e)

    scene(**yaml_config).run()


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
