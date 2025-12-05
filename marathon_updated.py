# marathon.py - Updated with obstacle avoidance
from line_sensor import LineReader
from drive import Motor
from machine import Pin, PWM
import math
from distance import Ultrasound
import time

# 1. --- Setup ---
# Instantiate your classes
lr = LineReader([Pin(5),Pin(4),Pin(3),Pin(2),Pin(1),Pin(0)], [-20,-12,-4, 4, 12, 20])
m = Motor()

# Set a base speed
velocity = 30

# PD Controller parameters
last_offset = 0.0
last_time_us = time.ticks_us() - 10000
Kp = 0.40  # Proportional gain
Kd = 0.01  # Derivative gain

# Ultrasound sensor
ultrasound = Ultrasound(trigger=Pin(28, Pin.OUT), echo=Pin(7, Pin.IN))

# Obstacle avoidance parameters
OBSTACLE_THRESHOLD = 10  # cm - distance to trigger avoidance
STATE_FOLLOWING = 0
STATE_AVOIDING = 1
STATE_SEARCHING = 2
current_state = STATE_FOLLOWING

def avoid_obstacle():
    """Execute obstacle avoidance maneuver"""
    # Stop briefly
    m.stop()
    time.sleep_ms(200)
    
    # Turn right to go around obstacle
    m.drive(0, math.radians(90))  # Turn right 90 degrees
    time.sleep_ms(600)
    m.stop()
    time.sleep_ms(100)
    
    # Drive forward past the obstacle
    m.drive(25, 0)
    time.sleep_ms(800)
    m.stop()
    time.sleep_ms(100)
    
    # Turn left to go back toward line
    m.drive(0, math.radians(-90))  # Turn left 90 degrees
    time.sleep_ms(600)
    m.stop()
    time.sleep_ms(100)
    
    # Drive forward to cross back over line
    m.drive(25, 0)
    time.sleep_ms(800)
    m.stop()
    time.sleep_ms(100)
    
    # Turn left again to realign with line
    m.drive(0, math.radians(-90))  # Turn left 90 degrees
    time.sleep_ms(600)
    m.stop()
    time.sleep_ms(200)

def search_for_line():
    """Search for the line by rotating slowly"""
    search_start = time.ticks_ms()
    max_search_time = 3000  # 3 seconds max search
    
    while time.ticks_diff(time.ticks_ms(), search_start) < max_search_time:
        lr.update()
        
        # If we find the line (low error), we're back on track
        if abs(lr.offset) < 15:
            return True
        
        # Rotate slowly to search
        m.drive(0, math.radians(45))
        time.sleep_ms(50)
    
    return False

try:
    while True:
        # Measure distance
        try:
            distance = ultrasound.measure()
        except TimeoutError:
            distance = 0  # Treat timeout as object detected
        
        # State machine for obstacle avoidance
        if current_state == STATE_FOLLOWING:
            # Check for obstacle
            if distance > 0 and distance <= OBSTACLE_THRESHOLD:
                current_state = STATE_AVOIDING
                avoid_obstacle()
                current_state = STATE_SEARCHING
                continue
            
            # Normal line following with PD controller
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
        
        elif current_state == STATE_SEARCHING:
            # Try to find the line again
            if search_for_line():
                current_state = STATE_FOLLOWING
                last_offset = 0.0
                last_time_us = time.ticks_us()
            else:
                # If we can't find line, try moving forward a bit
                m.drive(20, 0)
                time.sleep_ms(500)
                m.stop()
                time.sleep_ms(200)

finally:
    m.stop()
