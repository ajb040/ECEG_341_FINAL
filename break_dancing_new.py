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
    m = Motor()
    np = neopixel.NeoPixel(Pin(18),2)
    buzzer = PWM(Pin(22))

    # MOVE 1: Quick forward shimmy
    m.drive(15, 0)
    change_color((255,0,0))
    change_sound(1500,20000)
    time.sleep_ms(300)
    m.stop()
    time.sleep_ms(100)
    
    # MOVE 2: Quick back to center
    m.drive(-15, 0)
    change_color((0,255,0))
    change_sound(1200,18000)
    time.sleep_ms(300)
    m.stop()
    time.sleep_ms(100)
    
    # MOVE 3: Spin clockwise (in place)
    m.drive(0, math.radians(360))
    change_color((0,0,255))
    change_sound(1800,22000)
    time.sleep_ms(800)
    m.stop()
    time.sleep_ms(100)
    
    # MOVE 4: Wiggle right and back
    m.drive(10, math.radians(90))
    change_color((255,255,0))
    change_sound(900,15000)
    time.sleep_ms(350)
    m.drive(10, -math.radians(90))
    change_color((255,0,255))
    change_sound(1100,16000)
    time.sleep_ms(350)
    m.stop()
    time.sleep_ms(100)
    
    # MOVE 5: Spin counter-clockwise (in place)
    m.drive(0, -math.radians(360))
    change_color((0,255,255))
    change_sound(2000,24000)
    time.sleep_ms(800)
    m.stop()
    time.sleep_ms(100)
    
    # MOVE 6: Quick forward-back-forward combo
    m.drive(20, 0)
    change_color((128,0,255))
    change_sound(1400,19000)
    time.sleep_ms(250)
    m.drive(-20, 0)
    change_color((255,128,0))
    change_sound(1000,14000)
    time.sleep_ms(250)
    m.drive(20, 0)
    change_color((0,128,255))
    change_sound(1600,21000)
    time.sleep_ms(250)
    m.stop()
    time.sleep_ms(100)
    
    # MOVE 7: Back to center
    m.drive(-20, 0)
    change_color((255,255,255))
    change_sound(800,12000)
    time.sleep_ms(250)
    m.stop()
    time.sleep_ms(100)
    
    # MOVE 8: Half spin right, half spin left (wiggle)
    m.drive(0, math.radians(180))
    change_color((255,50,50))
    change_sound(2200,25000)
    time.sleep_ms(400)
    m.drive(0, -math.radians(180))
    change_color((50,255,50))
    change_sound(2400,26000)
    time.sleep_ms(400)
    m.stop()
    time.sleep_ms(100)
    
    # MOVE 9: Arc right (forward while turning)
    m.drive(15, math.radians(120))
    change_color((50,50,255))
    change_sound(1300,17000)
    time.sleep_ms(400)
    m.stop()
    time.sleep_ms(100)
    
    # MOVE 10: Arc left back to center
    m.drive(15, -math.radians(120))
    change_color((255,255,100))
    change_sound(1700,20000)
    time.sleep_ms(400)
    m.stop()
    time.sleep_ms(100)
    
    # MOVE 11: Fast double spin
    m.drive(0, math.radians(720))
    change_color((100,255,255))
    change_sound(2600,28000)
    time.sleep_ms(1200)
    m.stop()
    time.sleep_ms(100)
    
    # MOVE 12: Shimmy forward-back-forward-back
    m.drive(12, 0)
    change_color((255,100,255))
    change_sound(1100,15000)
    time.sleep_ms(200)
    m.drive(-12, 0)
    change_color((100,255,100))
    change_sound(1300,16000)
    time.sleep_ms(200)
    m.drive(12, 0)
    change_color((255,150,50))
    change_sound(1100,15000)
    time.sleep_ms(200)
    m.drive(-12, 0)
    change_color((50,150,255))
    change_sound(1300,16000)
    time.sleep_ms(200)
    m.stop()
    time.sleep_ms(100)
    
    # MOVE 13: Quick quarter turns alternating
    m.drive(8, math.radians(90))
    change_color((200,0,200))
    change_sound(1900,22000)
    time.sleep_ms(300)
    m.drive(8, -math.radians(90))
    change_color((0,200,200))
    change_sound(2100,23000)
    time.sleep_ms(300)
    m.drive(8, math.radians(90))
    change_color((200,200,0))
    change_sound(1900,22000)
    time.sleep_ms(300)
    m.drive(8, -math.radians(90))
    change_color((100,100,255))
    change_sound(2100,23000)
    time.sleep_ms(300)
    m.stop()
    time.sleep_ms(100)
    
    # MOVE 14: Forward diagonal sweep
    m.drive(12, math.radians(60))
    change_color((255,165,0))
    change_sound(1500,19000)
    time.sleep_ms(350)
    m.stop()
    time.sleep_ms(100)
    
    # MOVE 15: Back diagonal sweep
    m.drive(12, -math.radians(60))
    change_color((75,0,130))
    change_sound(1700,21000)
    time.sleep_ms(350)
    m.stop()
    time.sleep_ms(100)
    
    # MOVE 16: Rapid mini spins
    for i in range(4):
        m.drive(0, math.radians(180))
        change_color((255,0,0) if i % 2 == 0 else (0,255,0))
        change_sound(2000 + i*100, 23000)
        time.sleep_ms(250)
        m.stop()
        time.sleep_ms(50)
    
    # MOVE 17: Grand finale triple spin with color flash
    m.drive(0, math.radians(1080))
    for i in range(9):
        if i % 3 == 0:
            change_color((255,0,0))
        elif i % 3 == 1:
            change_color((0,255,0))
        else:
            change_color((0,0,255))
        change_sound(1800 + i*150, 25000)
        time.sleep_ms(200)
    m.stop()
    
    # Lights off, buzzer off
    change_color((0,0,0))
    buzzer.duty_u16(0)
    time.sleep_ms(500)
