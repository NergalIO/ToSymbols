#############################################
#############################################
##
##  Import modules
##
#############################################
#############################################

from threading import Thread
from PIL import Image
import numpy as np
import pyaudio
import moviepy
import pathlib
import random
import wave
import time
import cv2

#############################################
#############################################
##
##  Main Classes
##
#############################################
#############################################

class HighPrecisionSleep:
    def __init__(self, target_fps: int, ):
        self._target_fps = target_fps
        self._loop_delta = 1. / self._target_fps
        self._current_time = time.perf_counter()
        self._target_time = self._current_time
    
    def sleep(self) -> None:
        self._current_time = time.perf_counter()
        time.sleep(random.uniform(0, self._loop_delta / 2.))
        self._target_time += self._loop_delta
        sleep_time = self._target_time - time.perf_counter()
        if sleep_time > 0:
            time.sleep(sleep_time)


class FpsCounter:
    def __init__(self):
        self.st_time = time.time()
        self.cl_time = time.time()
        self.render_frames = 0
        self.total_frames = 0
        self.frames = 0
        
        self.getted_frames = 0
    
    def tick(self) -> None:
        if time.time() - self.cl_time >= 2:
            self.frames = 0
            self.render_frames = 0
            self.cl_time = time.time()
        self.render_frames += 1
        self.total_frames += 1
    
    def calculate_fps(self):
        try:
            return self.frames / (time.time() - self.cl_time)
        except ZeroDivisionError:
            pass
    
    def calculate_render_fps(self) -> None:
        try:
            return self.render_frames / (time.time() - self.cl_time)
        except ZeroDivisionError as e:
            pass
    
    def calculate_avarage_fps(self) -> None:
        try:
            return self.total_frames / (time.time() - self.st_time)
        except ZeroDivisionError:
            pass


class TimerBar:
    def __init__(self, total: int, width: int, video_height: int, fill: str) -> None:
        self.total = total
        self.n = 0
        
        self.width = width
        self.fill = fill
        
        self.percent_width = width / 100
        
        self.filled_bar = " " * self.width
        
        self.prefix = f"{preatty_time(self.n)}"
        self.bar = f"[{self.filled_bar}]"
        self.suffix = f"{preatty_time(self.total)}"
    
    def get_percent(self) -> int:
        try:
            return int((self.n / self.total) * 100)
        except ZeroDivisionError:
            return 0
    
    def get_percent_with_width(self) -> int:
        return int(self.get_percent() * self.percent_width)
    
    def update(self) -> None:
        self.prefix = f"{preatty_time(self.n)}"
        percent = self.get_percent_with_width()
        self.filled_bar = (self.fill * percent)  + (' ' * (self.width - percent))
        self.bar = f"[{self.filled_bar}]"
    
    def next(self, n: int = 1) -> None | bool:
        if self.n == self.total:
            return True
        self.n += n
        self.update()
    
    def __str__(self) -> str:
        return f"{self.prefix} {self.bar} {self.suffix}"


class FileConverter:
    @staticmethod
    def mp4_to_wav(path: str) -> str:
        if pathlib.Path(path.replace("mp4", "wav")).exists():
            return path.replace("mp4", "wav")
        video_file = moviepy.VideoFileClip(path)
        audio_file = video_file.audio
        audio_file.write_audiofile(path.replace("mp4", "wav"))
        return path.replace("mp4", "wav")


class SoundWav:
    def __init__(self, sound, fps):
        self.pyaudio = pyaudio.PyAudio()
        
        self.fps = fps
        self.sound = wave.open(sound)
        self.stream = self.pyaudio.open(
            format=pyaudio.get_format_from_width(self.sound.getsampwidth()),
            channels=self.sound.getnchannels(),
            rate=self.sound.getframerate(),
            output=True,
        )
    
    def stop(self) -> None:
        self.stream.close()
        self.pyaudio.terminate()
    
    def play_frame(self) -> None:
        data = self.sound.readframes(int(self.sound.getframerate()/self.fps))
        self.stream.write(data)


class SymbolVideo:
    def __init__(self, video_path: str, sound_path: str, new_height: int, buffer_size: int = 200):
        self._path = video_path
        self._new_height = new_height
        self._video = cv2.VideoCapture(video_path)
        
        if sound_path is not None:
            self._sound = SoundWav(sound_path, self._video.get(cv2.CAP_PROP_FPS))
            self._has_sound = True
        else:
            self._has_sound = False
        
        self._buffer_size = buffer_size
        self._buffer = []
        self._status = False
        self._missed_frames = 0
        
        self._fps_counter = FpsCounter()
        self._generator_thread = Thread(target=self._process)
    
    def get(self) -> str | None:
        if len(self._buffer) == 0:
            return None
        self._fps_counter.frames += 1
        self._fps_counter.getted_frames += 1
        return self._buffer.pop(0)
    
    def start(self) -> None:
        self._status = True
        self._generator_thread.start()
    
    def stop(self) -> None:
        self._status = False
        if self._has_sound:
            self._sound.stop()
    
    def _process(self) -> None:
        while self._status:
            ret, frame = self._video.read()
            if not ret:
                self._status = False
            while len(self._buffer) >= self._buffer_size:
                if self._status is False:
                    break
                time.sleep(0.01)
            self._buffer.append(frame_to_ascii(frame, self._new_height))
            self._fps_counter.tick()
    
    def play_audio_frame(self) -> None:
        self._sound.play_frame()
    
    def add_missed_frames(self) -> None:
        self._missed_frames += 1
    
    @property
    def height(self) -> int:
        return self._new_height
    
    @property
    def width(self) -> int:
        return int((self._new_height / self._video.get(cv2.CAP_PROP_FRAME_WIDTH)) * self._video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    @property
    def has_sound(self) -> bool:
        return self._has_sound
    
    @property
    def missed_frames(self) -> int:
        return self._missed_frames
    
    @property
    def buffer_size(self) -> int:
        return self._buffer_size
    
    @property
    def current_buffer_len(self) -> int:
        return len(self._buffer)
    
    @property
    def current_frame(self) -> int:
        return self._fps_counter.getted_frames
    
    @property
    def total_frames(self) -> int:
        return self._video.get(cv2.CAP_PROP_FRAME_COUNT)
    
    @property
    def total_time(self) -> int:
        return self.total_frames // self.video_fps - 8
    
    @property
    def current_time(self) -> int:
        return self.current_frame // self.video_fps
    
    @property
    def video_fps(self) -> int:
        return self._video.get(cv2.CAP_PROP_FPS)
    
    @property
    def render_fps(self) -> float:
        return self._fps_counter.calculate_render_fps()
    
    @property
    def current_fps(self) -> float:
        return self._fps_counter.calculate_fps()
    
    @property
    def avarage_fps(self) -> float:
        return self._fps_counter.calculate_avarage_fps()


class SymbolImage:
    def __init__(self, path: str, new_height: int) -> None:
        self._path = path
        self._new_height = new_height
        self._result = None
        
        self.image = Image.open(self._path)
        self.frame = np.zeros(
            shape=(
                self.image.height,
                self.image.width,
                len(self.image.getpixel((0, 0)))
            ),
            dtype=np.int16
        )
    
    def process_it(self) -> None:
        for y in range(self.image.height):
            for x in range(self.image.width):
                self.frame[y, x] = self.image.getpixel((x, y))
        self._result = frame_to_ascii(self.frame, self._new_height)
    
    @property
    def result(self) -> str | None:
        return self._result


#############################################
#############################################
##
##  Main Functions
##
#############################################
#############################################

def frame_to_ascii(frame: np.ndarray, new_height: int = None) -> str:
    if frame is None:
        raise ValueError("Frame must be not empty!")
    if new_height is not None:
        new_width = int((new_height / frame.shape[1]) * frame.shape[0])
        frame = cv2.resize(frame, (new_height, new_width), interpolation=cv2.INTER_AREA)
    ascii_image_array = to_symbols(frame)
    return "\n".join([ascii_image_array[y, :].tobytes().decode("latin-1") for y in range(ascii_image_array.shape[0])])

    
def to_symbols(frame: np.ndarray) -> np.vectorize:
    # Ñ@#W$9876543210!abc;:=-,._
    to_symbols = np.vectorize(lambda x: ("Ñ@#W$9876543210!abc;:=-,._")[-(x // 10)])
    avarages: np.ndarray = frame.mean(axis=2, dtype=np.integer)
    return to_symbols(avarages)


def preatty_time(time: int) -> str:
    days = int(time // 86400)
    hours = int(time // 3600) - (days * 24)
    minutes = int(time // 60) - (hours * 60)
    seconds = int(time % 60)
    
    result = []
    
    if days > 0:
        result.append(f"{days}")
    
    if hours > 1 < 10:
        result.append(f"0{hours}")
    elif hours >= 10:
        result.append(f"{hours}")
    
    if minutes < 10:
        result.append(f"0{minutes}")
    else:
        result.append(f"{minutes}")
    
    if seconds < 10:
        result.append(f"0{seconds}")
    else:
        result.append(f"{seconds}")
    
    return ":".join(result)