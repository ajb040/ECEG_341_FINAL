# line_follow.py
from line_sensor import LineReader
from drive import Motor
from machine import Pin, PWM
import time

# 1. --- Setup ---
# Instantiate your classes
lr = LineReader([Pin(5),Pin(4),Pin(3),Pin(2),Pin(1),Pin(0)], [-20,-12,-4, 4, 12, 20]) # Assuming default pins/positions

m = Motor() # you might have different constructor values

# Set a base speed. 30 is a good start.
velocity = 36

# 2. --- Control Loop ---
last_offset = 0.0
last_time_us = time.ticks_us() - 10000 # Initialize in the past

Kp = 0.40 # Proportional gain
Kd = 0.01 # Derivative gain (start with a small value!)

try:
    for i in range(1500): # run for 500 iterations then stop!
        # Calculate dt (time delta)
        current_time_us = time.ticks_us()
        dt_us = time.ticks_diff(current_time_us, last_time_us)
        dt_s = dt_us / 1000000.0 # convert to seconds
        last_time_us = current_time_us


        # Get the latest sensor reading
        lr.update()

        # --- IMPLEMENT YOUR CONTROL LOGIC HERE ---
        #
        # 1. Calculate the 'error' (which is just lr.offset)
        error = lr.offset
        # 2. Calculate the 'angular_velocity' based on the error
        #
        # --- P-Only Control Logic ---
        error = lr.offset

        derivative = 0
        if dt_s > 0:
            derivative = (error - last_offset) / dt_s

        
        angular_velocity = (Kp * error) + (Kd * derivative)

        last_offset = error
        # --- END CONTROL LOGIC ---
        #
        # --- END CONTROL LOGIC ---
        

        # Send the command to the motors
        # Note: We use -angular_velocity if your motor
        # class defines a positive angle as a left turn.
        # This depends on your motor.drive() implementation.
        # Let's start by assuming a positive value turns right.
        m.drive(velocity,angular_velocity)
               
        # A small delay is not needed if your loop
        # is fast, but 1ms can be okay. (try differnt values!)
        time.sleep_ms(1)

finally:
    m.stop() # Always stop the motors

