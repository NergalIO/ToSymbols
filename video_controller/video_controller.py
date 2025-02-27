from handlers import Converter, clear, fast_rewrite, TimerBar, HighPrecisionSleep, VideoToSoundConverter, SoundWav, resize
from threading import Thread
import keyboard
import time
import cv2


class VideoController:
    def __init__(self):
        pass


class VideoConverterToASCII(Converter):
    def __init__(self, video_path: str, new_height: int = None, colorize: bool = False, input_buffer_size: int = 200, output_buffer_size: int = 200):
        self.path = video_path
        self.video = cv2.VideoCapture(video_path)
        self.sound = SoundWav(VideoToSoundConverter.mp4_to_wav(video_path), self.video.get(cv2.CAP_PROP_FPS))
        
        clear()
        if new_height is None:
            new_height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)        
        
        self._missed_frames = 0
        
        self.to_buffer_status = "Stopped"
        self.to_buffer_thread = Thread(target=self.to_buffer)
        
        super().__init__(new_height, colorize, input_buffer_size, output_buffer_size)
    
    def start(self) -> None:
        try:
            self.converter_status = "Working"
            self.to_buffer_status = "Working"
            
            self.converter_thread.start()
            self.to_buffer_thread.start()
            
            sleep = HighPrecisionSleep(self.video_fps)
            timer = TimerBar(self.total_time, self.width, self.height, "*")
            
            while self.converter_status == "Working":
                try: 
                    if keyboard.is_pressed("q"):
                        break
                    
                    while len(self.output_buffer) == 0:
                        if self.converter_status == "Stopped":
                            break
                        time.sleep(0.01)
                    
                    text = self.get_converted()
                    text += f"\n{' ' * 100}\n{timer}{' ' * 100}\n"
                    text += f"\n{' ' * 100}\nStatistics:{' ' * 100}\n{' ' * 100}\nFrames: {self.current_frame}{' ' * 100}\n" +\
                            f"Current FPS: {self.current_fps:.1f}, Render FPS: {self.render_fps:.1f}{' ' * 100}\n" +\
                            f"Missed frames: {self.missed_frames}{' ' * 100}\nInput Buffer: {len(self.input_buffer)}/{self.input_buffer_size}{' ' * 100}" +\
                            f"\nOutput Buffer: {len(self.output_buffer)}/{self.output_buffer_size}{' ' * 100}"
                    
                    fast_rewrite(text, self.new_height)
                    self.sound.play_frame()
                    
                    timer.n = self.current_time
                    timer.update()
                    
                    sleep.sleep()
                except TypeError:
                    self._missed_frames += 1
                    self.sound.play_frame()
        finally:
            print("\033[0m")
            self.stop()
            self.to_buffer_status = "Stopped"
            clear()
            print("\n\t\tStatistics:\n")
            print(f"\tFrames: {self.current_frame}")
            print(f"\tMissed Frames: {self.missed_frames}")
            print(f"\tAvarage FPS: {self.avarage_fps}\n\n")
    
    def to_buffer(self) -> None:
        while self.to_buffer_status == "Working":
            ret, frame = self.video.read()
            if not ret:
                self.to_buffer_status = "Stopped"
                break
            while len(self.input_buffer) >= self.input_buffer_size:
                if self.to_buffer_status == "Stopped":
                    break
                time.sleep(0.1)
            self.add_to_convert(frame)
    
    @property
    def height(self) -> int:
        return self.new_height
    
    @property
    def width(self) -> int:
        return int((self.new_height / self.video.get(cv2.CAP_PROP_FRAME_WIDTH)) * self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    @property
    def missed_frames(self) -> int:
        return self._missed_frames
    
    @property
    def current_frame(self) -> int:
        return self.fps_controller.frames
    
    @property
    def total_frames(self) -> int:
        return self.video.get(cv2.CAP_PROP_FRAME_COUNT)
    
    @property
    def total_time(self) -> int:
        return self.total_frames // self.video_fps
    
    @property
    def current_time(self) -> int:
        return self.current_frame // self.video_fps
    
    @property
    def video_fps(self) -> int:
        return self.video.get(cv2.CAP_PROP_FPS)
    
    @property
    def render_fps(self) -> float:
        return self.fps_controller.calculate_render_fps()
    
    @property
    def current_fps(self) -> float:
        return self.fps_controller.calculate_fps()
    
    @property
    def avarage_fps(self) -> float:
        return self.fps_controller.calculate_avarage_fps()
            