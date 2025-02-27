from . import fps_controller
from threading import Thread
import numpy as np
import colorama
import time
import cv2

import warnings
warnings.filterwarnings("ignore")

colorama.init()

class Converter:
    def __init__(self, new_height: int = None, colorize: bool = False, input_buffer_size: int = 100, output_buffer_size: int = 100):
        self.new_height = new_height
        self.colorize = colorize
        
        self.input_buffer_size = input_buffer_size
        self.output_buffer_size = output_buffer_size
        
        self.input_buffer = []
        self.output_buffer = []
        
        self.converter_thread = Thread(target=self.converter_loop)
        self.converter_status = "Stopped"
        
        self.to_ascii_alg = np.vectorize(lambda x: (" .:!/r(lZ4H9W8$@")[x // 16])
        
        self.fps_controller = fps_controller.FpsCounter()
    
    def start(self) -> None:
        self.converter_status = "Working"
        self.converter_thread.start()
    
    def stop(self) -> None:
        self.converter_status = "Stopped"
    
    def converter_loop(self) -> None:
        while self.converter_status == "Working":
            while len(self.input_buffer) == 0 or len(self.output_buffer) >= self.output_buffer_size:
                if self.converter_status == "Stopped":
                    break
                time.sleep(0.01)
            self.output_buffer.append(self.convert(self.input_buffer.pop(0), self.new_height))
            self.fps_controller.tick()
    
    def convert(self, frame: np.ndarray, new_height: int) -> str:
        if frame is None:
            raise ValueError("Frame must be not empty!")
        if new_height is not None:
            new_width = int((new_height / frame.shape[1]) * frame.shape[0])
            frame = cv2.resize(frame, (new_height, new_width), interpolation=cv2.INTER_AREA)
        
        if not self.colorize:
            avarages = frame.mean(axis=2, dtype=np.integer)
            ascii_image_array = self.to_ascii_alg(avarages)
        else:
            ascii_image_array = np.apply_along_axis(
                self._colorized_convert_alg,
                axis=2,
                arr=frame
            )
        return "\n".join([ascii_image_array[y, :].tobytes().decode("latin-1") for y in range(ascii_image_array.shape[0])]) + "\033[0m"
    
    def _colorized_convert_alg(self, pixel: np.ndarray) -> str:
        #letter = (" .:!/r(lZ4H9W8$@")[-(sum(pixel) // 3) // 16]
        #if letter == " ":
        #    return " "
        R, G, B = pixel
        return f"\033[48;2;{B};{G};{R}m "
    
    def add_to_convert(self, frame: np.ndarray) -> None:
        self.input_buffer.append(frame)
    
    def get_converted(self) -> str:
        self.fps_controller.frames += 1
        self.fps_controller.getted_frames += 1
        return self.output_buffer.pop(0)
    