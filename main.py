import camera_controller
import video_controller
import pathlib
import sys


if len(sys.argv) == 1:
    exit("Usage: python main.py [--video, --camera] [args] [path (if video)]")


match sys.argv[1]:
    case "--video":
        kwargs = {}
        for arg in sys.argv[2:]:
            if "=" in arg:
                arg, value = arg.split("=")
            else:
                value = None
            
            match arg:
                case "--path":
                    if value is None:
                        raise ValueError("path to video file must be not empty!")
                    kwargs['video_path'] = value
                case "--new-height":
                    if value is None:
                        kwargs['new_height'] = 128
                    else:
                        kwargs['new_height'] = int(value)
                case "--colorize":
                    if value is None:
                        kwargs['colorize'] = True
                case _:
                    if pathlib.Path(arg).exists():
                        kwargs['video_path'] = arg
                    else:
                        exit(f"Unknown argument with name <{arg}>!")
        try:
            video = video_controller.VideoConverterToASCII(**kwargs)
            video.start()
        except Exception as e:
            video.stop()
            exit(e)
            
    case "--camera":
        kwargs = {}
        for arg in sys.argv[2:]:
            if "=" in arg:
                arg, value = arg.split("=")
            else:
                value = None
            
            match arg:
                case "--new-height":
                    if value is None:
                        kwargs['new_height'] = 128
                    else:
                        kwargs['new_height'] = int(value)
                case "--colorize":
                    if value is None:
                        kwargs['colorize'] = True
                case _:
                    exit(f"Unknown argument with name <{arg}>!")
        
        try:
            camera = camera_controller.CameraConverterToASCII(**kwargs)
            camera.start()
        except Exception as e:
            camera.stop()
            exit(e)
    case _:
        exit("Usage: python main.py [--video, --camera] [args] [path (if video)]")

"""
import camera_controller

camera = camera_controller.CameraConverterToASCII(64, True)
camera.start()


"""