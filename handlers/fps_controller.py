import time


class FpsCounter:
    def __init__(self):
        self.st_time = time.time()
        self.cl_time = time.time()
        self.render_frames = 0
        self.total_frames = 0
        self.getted_frames = 0
        
        self.frames = 0
    
    def tick(self) -> None:
        if time.time() - self.cl_time >= 2:
            self.getted_frames = 0
            self.render_frames = 0
            self.cl_time = time.time()
        self.render_frames += 1
        self.total_frames += 1
    
    def calculate_fps(self):
        try:
            return self.getted_frames / (time.time() - self.cl_time)
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