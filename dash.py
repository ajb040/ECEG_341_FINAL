# line_follow.py
from line_sensor import LineReader
from drive import Motor
from machine import Pin, PWM
from distance import Ultrasound
import time

# 1. --- Setup ---
# Instantiate your classes
lr = LineReader([Pin(5),Pin(4),Pin(3),Pin(2),Pin(1),Pin(0)], [-20,-12,-4, 4, 12, 20]) # Assuming default pins/positions

m = Motor() # you might have different constructor values

# Set a base speed. 30 is a good start.
velocity = 30 

# 2. --- Control Loop ---
last_offset = 0.0
last_time_us = time.ticks_us() - 10000 # Initialize in the past

Kp = 0.40 # Proportional gain
Kd = 0.01 # Derivative gain (start with a small value!)

ultrasound = Ultrasound(trigger = Pin(28, Pin.OUT), echo = Pin(7, Pin.IN))

try:
    while True:
        try:
            distance = ultrasound.measure()
        except TimeoutError:
            distance = 0      # treat as object detected
        
        # STOP CONDITION
        if distance <= 20:
            m.stop()
            time.sleep_ms(50)
            continue
    
        # FOLLOW LINE (safe distance)
        current_time_us = time.ticks_us()
        dt_us = time.ticks_diff(current_time_us, last_time_us)
        dt_s = dt_us / 1_000_000
        last_time_us = current_time_us
    
        lr.update()
        error = lr.offset
    
        derivative = 0
        if dt_s > 0:
            derivative = (error - last_offset) / dt_s
    
        angular_velocity = Kp * error + Kd * derivative
        last_offset = error
    
        m.drive(velocity, angular_velocity)
        time.sleep_ms(1)
        else:
            m.stop()

finally:

    m.stop() # Always stop the motors
