import random
import time


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