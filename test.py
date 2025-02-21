import handler
import time

bar = handler.TimerBar(10, 50, "*")

while bar.next() is None:
    print(bar)
    time.sleep(1)