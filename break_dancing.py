import machine 
from machine import Pin, PWM
import time
import math
import neopixel
from drive import Motor

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



def change_color(color):
    for i in range (len(np)):
        np[i] = color
    np.write()

def change_sound(freq,duty):
    buzzer.freq(freq)
    buzzer.duty_u16(duty)



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
    np = neopixel.NeoPixel(Pin(18),2)
    buzzer = PWM(Pin(22))

    m.drive (20, 0)
    change_color((255,0,0))
    change_sound(1500,20000)
    time.sleep_ms(500)
    # stop, robot should have gone 10 cm forward. Check! I got about 12 cm.
    m.drive (0, 0)
    time.sleep_ms(500)


    # TEST 2 -- reverse
    # -20 cm/s, 0 rad/s 
    m.drive (-20, 0)
    change_color((0,255,0))
    change_sound(1000,12000)
    time.sleep_ms(500)
    # stop, robot should have gone 10 cm in reverse. Drive the M1B and M2B pins!
    m.drive (0, 0)
    time.sleep_ms(500)



    # TEST 3 -- RIGHT
    m.drive (20, math.radians(180))
    change_color((0,0,255))
    change_sound(700,6000)
    time.sleep_ms(500)
    # stop, robot should have turned about 90 degrees clockwise
    m.drive (0, 0)
    time.sleep_ms(500)


    # TEST 4 -- LEFT
    m.drive (20, -math.radians(180))
    change_color((255,255,0))
    change_sound(500,4000)
    time.sleep_ms(500)
    # stop, we should have turned about 180 degrees counter clockwise
    m.drive (0, 0)
    time.sleep_ms(500)



    # TEST 5 -- ROTATE in PLACE
    m.drive (0, math.radians(360))
    change_color((0,255,255))
    change_sound(300,2000)
    time.sleep_ms(1000)
    # stop, robot should turn about 360 degrees clockwise
    m.drive (0, 0)
    time.sleep_ms(500)