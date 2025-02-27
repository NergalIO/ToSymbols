from handlers import Converter, clear, fast_rewrite
import numpy as np
import keyboard
import time
import cv2


class CameraController:
    def __init__(self, device_id = 0):
        self.camera = cv2.VideoCapture(device_id)
        
        self.size = (int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
                     int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        self.fps = self.camera.get(cv2.CAP_PROP_FPS)
    
    def imshow(self) -> None:
        while True:
            frame = self.get_current_frame()
            
            cv2.imshow("Camera", frame)
            
            if cv2.waitKey(1) == ord('q'):
                break
    
    def get_current_frame(self) -> np.ndarray:
        frame = self.camera.read()[1]
        if frame is None:
            raise cv2.error("Camera device not found!")
        return frame



class CameraConverterToASCII(Converter):
    def __init__(self, new_height = None, colorize: bool = False, input_buffer_size = 100, output_buffer_size = 200):
        self.camera_controller = CameraController()
        
        if new_height is None:
            new_height = self.camera_controller.size[0]
        
        self._missed_frames = 0
        
        super().__init__(new_height, colorize, input_buffer_size, output_buffer_size)
    
    def start(self) -> None:
        try:
            self.converter_status = "Working"
            self.converter_thread.start()
            
            clear()
            while self.converter_status == "Working":
                try:
                    if keyboard.is_pressed("q"):
                        break
                    
                    frame = self.camera_controller.get_current_frame()
                    self.add_to_convert(frame)
                    
                    while len(self.output_buffer) == 0:
                        if self.converter_status == "Stopped":
                            break
                        time.sleep(0.01)
                    
                    text = self.get_converted()
                    text += f"\n{' ' * 100}\nStatistics:{' ' * 100}\n{' ' * 100}\nFrames: {self.current_frame}{' ' * 100}\n" +\
                            f"Current FPS: {self.current_fps:.1f}, Render FPS: {self.render_fps:.1f}{' ' * 100}\n" +\
                            f"Missed frames: {self.missed_frames}{' ' * 100}\nInput Buffer: {len(self.input_buffer)}/{self.input_buffer_size}{' ' * 100}" +\
                            f"\nOutput Buffer: {len(self.output_buffer)}/{self.output_buffer_size}{' ' * 100}"
                    
                    fast_rewrite(text, self.new_height)
                except TypeError:
                    self._missed_frames += 1
        finally:
            self.stop()
            clear()
            print("\n\t\tStatistics:\n")
            print(f"\tFrames: {self.current_frame}")
            print(f"\tMissed Frames: {self.missed_frames}")
            print(f"\tAvarage FPS: {self.avarage_fps}\n\n")
    
    @property
    def missed_frames(self) -> int:
        return self._missed_frames
    
    @property
    def current_frame(self) -> int:
        return self.fps_controller.total_frames
    
    @property
    def current_fps(self) -> float:
        return self.fps_controller.calculate_fps()
    
    @property
    def avarage_fps(self) -> float:
        return self.fps_controller.calculate_avarage_fps()
    
    @property
    def render_fps(self) -> float:
        return self.fps_controller.calculate_render_fps()
            