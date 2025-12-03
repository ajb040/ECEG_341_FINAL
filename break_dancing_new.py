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
    
    # Imperial March melody - (frequency, duration_ms)
    melody = [
        (392, 500), (392, 500), (392, 500),  # G G G
        (311, 350), (466, 150),               # Eb Bb
        (392, 500), (311, 350), (466, 150),   # G Eb Bb
        (392, 1000),                          # G (hold)
        (587, 500), (587, 500), (587, 500),  # D D D
        (622, 350), (466, 150),               # Eb Bb
        (370, 500), (311, 350), (466, 150),   # F# Eb Bb
        (392, 1000),                          # G (hold)
    ]

    # MOVE 1: Big forward charge! (G)
    m.drive(30, 0)
    change_color((255,0,0))
    change_sound(melody[0][0], 20000)
    time.sleep_ms(melody[0][1])
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 2: Continue forward (G)
    m.drive(30, 0)
    change_color((255,50,0))
    change_sound(melody[1][0], 20000)
    time.sleep_ms(melody[1][1])
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 3: One more forward push (G)
    m.drive(30, 0)
    change_color((255,100,0))
    change_sound(melody[2][0], 20000)
    time.sleep_ms(melody[2][1])
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 4: Quick turn (Eb)
    m.drive(0, math.radians(180))
    change_color((0,255,0))
    change_sound(melody[3][0], 20000)
    time.sleep_ms(melody[3][1])
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 5: Quick burst (Bb)
    m.drive(25, math.radians(90))
    change_color((0,255,100))
    change_sound(melody[4][0], 22000)
    time.sleep_ms(melody[4][1])
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 6: Straight forward (G)
    m.drive(30, 0)
    change_color((0,255,255))
    change_sound(melody[5][0], 20000)
    time.sleep_ms(melody[5][1])
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 7: Side arc (Eb)
    m.drive(20, -math.radians(90))
    change_color((0,150,255))
    change_sound(melody[6][0], 20000)
    time.sleep_ms(melody[6][1])
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 8: Forward burst (Bb)
    m.drive(25, math.radians(60))
    change_color((0,100,255))
    change_sound(melody[7][0], 22000)
    time.sleep_ms(melody[7][1])
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 9: Big spin (G hold)
    m.drive(0, math.radians(720))
    change_color((100,0,255))
    change_sound(melody[8][0], 20000)
    time.sleep_ms(melody[8][1])
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 10: Forward burst (D)
    m.drive(30, 0)
    change_color((255,0,255))
    change_sound(melody[9][0], 20000)
    time.sleep_ms(melody[9][1])
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 11: Continue forward (D)
    m.drive(30, 0)
    change_color((255,0,200))
    change_sound(melody[10][0], 20000)
    time.sleep_ms(melody[10][1])
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 12: Forward again (D)
    m.drive(30, 0)
    change_color((255,0,150))
    change_sound(melody[11][0], 20000)
    time.sleep_ms(melody[11][1])
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 13: Spin left (Eb)
    m.drive(0, -math.radians(180))
    change_color((255,100,100))
    change_sound(melody[12][0], 20000)
    time.sleep_ms(melody[12][1])
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 14: Arc right (Bb)
    m.drive(25, math.radians(90))
    change_color((255,150,0))
    change_sound(melody[13][0], 22000)
    time.sleep_ms(melody[13][1])
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 15: Diagonal move (F#)
    m.drive(20, -math.radians(120))
    change_color((200,200,0))
    change_sound(melody[14][0], 20000)
    time.sleep_ms(melody[14][1])
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 16: Back diagonal (Eb)
    m.drive(20, math.radians(60))
    change_color((100,255,100))
    change_sound(melody[15][0], 20000)
    time.sleep_ms(melody[15][1])
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 17: Quick burst (Bb)
    m.drive(25, -math.radians(90))
    change_color((150,255,150))
    change_sound(melody[16][0], 22000)
    time.sleep_ms(melody[16][1])
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 18: Grand finale spin (G hold)
    m.drive(0, math.radians(1080))
    change_sound(melody[17][0], 20000)
    for i in range(8):
        if i % 3 == 0:
            change_color((255,0,0))
        elif i % 3 == 1:
            change_color((0,255,0))
        else:
            change_color((0,0,255))
        time.sleep_ms(125)
    m.stop()
    
    # Quick celebration shimmy!
    change_sound(523, 18000)  # C
    m.drive(20, 0)
    change_color((255,255,0))
    time.sleep_ms(200)
    m.drive(-20, 0)
    change_color((0,255,255))
    time.sleep_ms(200)
    m.drive(20, 0)
    change_color((255,0,255))
    time.sleep_ms(200)
    m.stop()
    
    # Lights off, buzzer off
    change_color((0,0,0))
    buzzer.duty_u16(0)
    time.sleep_ms(500)
