import numpy as np
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