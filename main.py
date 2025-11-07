from line_sensor import LineReader
from machine import Pin
import time

if __name__ == "__main__":
    lr = LineReader([Pin(5),Pin(4),Pin(3),Pin(2),Pin(1),Pin(0)], [-20,-12,-4, 4, 12, 20])

    while True:
        lr.update()
        print(f"Offset: {lr.offset:4.2f}")
        time.sleep(0.1)
