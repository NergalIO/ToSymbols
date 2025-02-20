import numpy as np
import handler
import cv2


class CameraController:
    def __init__(self, device_id = 0):
        self.camera = cv2.VideoCapture(device_id)
        
        self.size = (int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
                     int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        self.fps = self.camera.get(cv2.CAP_PROP_FPS)
        
        self._missed_frames = 0
        self._fps_counter = handler.FpsCounter()
    
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
        self._fps_counter.getted_frames += 1
        self._fps_counter.total_frames += 1
        self._fps_counter.frames += 1
        return frame
    
    def add_missed_frames(self) -> None:
        self._missed_frames += 1
    
    @property
    def missed_frames(self) -> int:
        return self._missed_frames
    
    @property
    def current_frame(self) -> int:
        return self._fps_counter.getted_frames
    
    @property
    def current_fps(self) -> float:
        return self._fps_counter.calculate_fps()
    
    @property
    def avarage_fps(self) -> float:
        return self._fps_counter.calculate_avarage_fps()
    
    @property
    def render_fps(self) -> float:
        return self._fps_counter.calculate_render_fps()