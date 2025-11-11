import machine 
from machine import Pin, PWM
import time
import math

class MotorDriver:
    """Represents one side of the robot (two PWM pins controlling direction)."""
    def __init__(self, pin_forward: int, pin_backward: int, freq: int = 8000):
        self.forward = PWM(Pin(pin_forward))
        self.backward = PWM(Pin(pin_backward))
        self.forward.freq(freq)
        self.backward.freq(freq)

    def set_speed(self, duty: int):
        """Set motor speed with signed duty cycle (0–65535 range)."""
        duty = max(min(abs(int(duty)), 65535), 0)
        if duty == 0:
            self.forward.duty_u16(0)
            self.backward.duty_u16(0)
        elif duty > 0:
            self.forward.duty_u16(duty)
            self.backward.duty_u16(0)
        else:
            self.forward.duty_u16(0)
            self.backward.duty_u16(duty)

    def stop(self):
        #Stop motor completely
        self.forward.duty_u16(0)
        self.backward.duty_u16(0)


class Motor:
    def __init__(self,freq = 8_000):
        self.M1A = machine.PWM(machine.Pin(8))
        self.M1B = machine.PWM(machine.Pin(9))
        self.M2A = machine.PWM(machine.Pin(10))
        self.M2B = machine.PWM(machine.Pin(11))
        self.M1A.freq(freq)
        self.M1B.freq(freq)
        self.M2A.freq(freq)
        self.M2B.freq(freq)

    def drive(self, speed, omega):
        L = 13

        v_L = (speed) - ((-omega * L)/2)
        v_R = (speed) + ((-omega * L)/2)
        PWM_L = abs(1000*v_L) + 6152
        PWM_R = abs(1000*v_R) + 6152
        if v_L >= 0:
            self.M1A.duty_u16(int(PWM_L)) 
            self.M1B.duty_u16(0)
        else:
            self.M1A.duty_u16(0) 
            self.M1B.duty_u16(int(PWM_L)) 
        if v_R > 0:
            self.M2A.duty_u16(int(PWM_R))
            self.M2B.duty_u16(0)
        else:
            self.M2A.duty_u16(0)
            self.M2B.duty_u16(int(PWM_R))

    def drive_curl(self,speed,omega):
        L = 13

        bias = -.10
        # split bias to left/right motors 
        left_bias = 1.0 - bias/2 
        right_bias = 1.0 + bias/2

        v_L = (speed) - ((-omega * L)/2)
        v_R = (speed) + ((-omega * L)/2)
        PWM_L = abs(1000*v_L) + 6152
        PWM_R = abs(1000*v_R) + 6152
        PWM_L = int(PWM_L * left_bias)
        PWM_R = int(PWM_L * right_bias)
        if v_L >= 0:
            self.M1A.duty_u16(int(PWM_L)) 
            self.M1B.duty_u16(0)
        else:
            self.M1A.duty_u16(0) 
            self.M1B.duty_u16(int(PWM_L)) 
        if v_R > 0:
            self.M2A.duty_u16(int(PWM_R))
            self.M2B.duty_u16(0)
        else:
            self.M2A.duty_u16(0)
            self.M2B.duty_u16(int(PWM_R))


    def stop(self):
        self.M1A.duty_u16(0)
        self.M1B.duty_u16(0)
        self.M2A.duty_u16(0)
        self.M2B.duty_u16(0)
    




# 0 = even, >0 = bias right, <0 = bias left
bias = -.07

# split bias to left/right motors 
left_bias = 1.0 - bias/2 
right_bias = 1.0 + bias/2

#Sets speed and adjusts for bias
speed = 30
speed_duty = 1000*speed + 6152
speed_bias_left = int(speed_duty * left_bias)
speed_bias_right = int(speed_duty * right_bias)

'''
M1A.duty_u16(speed_bias_left) 
M1B.duty_u16(0) 
M2A.duty_u16(speed_bias_right)
M2B.duty_u16(0) 

time.sleep(5) # stop M1A.duty_u16(0)
M1A.duty_u16(0)
M2A.duty_u16(0)
'''


if __name__ == "__main__":
    # TEST 1 -- straight!
    # 20 cm/s, 0 rad/s 
    m = Motor()
    m.drive (20, 0)
    time.sleep_ms(500)
    # stop, robot should have gone 10 cm forward. Check! I got about 12 cm.
    m.drive (0, 0)
    time.sleep_ms(500)


    # TEST 2 -- reverse
    # -20 cm/s, 0 rad/s 
    m.drive (-20, 0)
    time.sleep_ms(500)
    # stop, robot should have gone 10 cm in reverse. Drive the M1B and M2B pins!
    m.drive (0, 0)
    time.sleep_ms(500)



    # TEST 3 -- RIGHT
    m.drive (20, math.radians(180))
    time.sleep_ms(500)
    # stop, robot should have turned about 90 degrees clockwise
    m.drive (0, 0)
    time.sleep_ms(500)


    # TEST 4 -- LEFT
    m.drive (20, -math.radians(180))
    time.sleep_ms(500)
    # stop, we should have turned about 180 degrees counter clockwise
    m.drive (0, 0)
    time.sleep_ms(500)



    # TEST 5 -- ROTATE in PLACE
    m.drive (0, math.radians(360))
    time.sleep_ms(1000)
    # stop, robot should turn about 360 degrees clockwise
    m.drive (0, 0)
    time.sleep_ms(500)
