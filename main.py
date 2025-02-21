#############################################
#############################################
##
##  Import modules
##
#############################################
#############################################

from CameraController import CameraController
import keyboard
import handler
import core
import tqdm
import sys
import os

#############################################
#############################################
##
##  Aliases
##
#############################################
#############################################

if sys.platform == "linux" or sys.platform == "linux2":
    clear = lambda: os.system("clear")
elif sys.platform == "win32":
    clear = lambda: os.system("cls")

#############################################
#############################################
##
##  Commands For Console Core
##
#############################################
#############################################

def show_camera(new_height: int) -> None:
    camera = CameraController()
    clear()
    try:
        while True:
            try:
                if keyboard.is_pressed("q"):
                    break
            
                frame = camera.get_current_frame()
                frame = handler.frame_to_ascii(frame, new_height)
                camera._fps_counter.tick()
                
                sys.stdout.write("\033[F" * new_height)
                sys.stdout.write(frame)
                sys.stdout.write(
                    f"\n{' ' * 100}\nStatistics:{' ' * 100}\n{' ' * 100}\nFrames: {camera.current_frame}{' ' * 100}\n" +\
                    f"Current FPS: {camera.current_fps:.1f}, Render FPS: {camera.render_fps:.1f}{' ' * 100}\n" +\
                    f"Missed frames: {camera.missed_frames}{' ' * 100}"
                )
                sys.stdout.flush()
            except TypeError:
                camera.add_missed_frames()
                continue
    except Exception as e:
        print(e)
    finally:
        clear()
        print("Statistics:")
        print(f"\tFrames: {camera.current_frame}")
        print(f"\tMissed Frames: {camera.missed_frames}")
        print(f"\tAvarage FPS: {camera.avarage_fps}")


def image_to_symbols(path: str, new_height: int) -> None:
    symbol_image = handler.SymbolImage(path, new_height)
    symbol_image.process_it()
    clear()
    print(symbol_image.result, flush=True)

def video_to_symbols(path: str, new_height: int) -> None:
    try:
        sound_path = handler.FileConverter.mp4_to_wav(path)
        clear()
        
        video = handler.SymbolVideo(path, sound_path, new_height, 200)
        video.start()

        timer_bar = handler.TimerBar(video.total_time, video.width, video.height, "#")
        
        high_preccision_sleep = handler.HighPrecisionSleep(video.video_fps)
        while True:
            try:    
                frame = video.get()
                
                if keyboard.is_pressed("q") or video._status is False:
                    video.stop()
                    break
                
                sys.stdout.write("\033[F" * new_height * 10 + frame)
                sys.stdout.write(
                    f"\n\n{' ' * 20}\n{timer_bar}{' ' * 20}\n" +\
                    f"{' ' * 20}\nStatistics:{' ' * 100}\n{' ' * 20}\nFrames: {video.current_frame}/{video.total_frames}{' ' * 20}\n" +\
                    f"Current FPS: {video.current_fps:.1f}, Render FPS: {video.render_fps:.1f}{' ' * 20}\nBuffer: {video.current_buffer_len}/{video.buffer_size}{' ' * 20}\n" +\
                    f"Missed frames: {video.missed_frames}{' ' * 20}"
                )
                sys.stdout.flush()
                
                if video.has_sound:
                    video.play_audio_frame()
                
                timer_bar.n = video.current_time
                timer_bar.update()
                high_preccision_sleep.sleep()
            except TypeError as e:
                video.add_missed_frames()
                video.play_audio_frame()
                continue
    finally:
        video.stop()
        clear()
        print("Statistics:")
        print(f"\tFrames: {video.current_frame}/{video.total_frames}")
        print(f"\tMissed Frames: {video.missed_frames}")
        print(f"\tAvarage FPS: {video.avarage_fps}")
        

    

#############################################
#############################################
##
##  Init commands
##
#############################################
#############################################

show_camera_command = core.Command(
    "show_camera",
    "Show camera by the ascii symbols",
    show_camera,
    {"new_height": (int, None)}
)

image_to_symbols_command = core.Command(
    "image_to_symbols",
    "Show image by the ascii symbols",
    image_to_symbols,
    {"path": str, "new_height": (int, None)}
)

video_to_symbols_command = core.Command(
    "video_to_symbols",
    "Playback video by the ascii symbols",
    video_to_symbols,
    {"path": str, "new_height": (int, None)}
)

#############################################
#############################################
##
##  Start Console Core
##
#############################################
#############################################

c_core = core.Console([show_camera_command, image_to_symbols_command, video_to_symbols_command])
c_core.loop()