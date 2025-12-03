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
    
    # Song: "Imperial March" melody (Star Wars)
    # Notes: (frequency_hz, duration_ms)
    melody = [
        (392, 400), (392, 400), (392, 400),  # G G G
        (311, 300), (466, 100),               # Eb Bb
        (392, 400), (311, 300), (466, 100),   # G Eb Bb
        (392, 800),                           # G (hold)
        (587, 400), (587, 400), (587, 400),  # D D D
        (622, 300), (466, 100),               # Eb Bb
        (370, 400), (311, 300), (466, 100),   # F# Eb Bb
        (392, 800),                           # G (hold)
    ]
    
    note_index = 0
    
    def play_next_note():
        nonlocal note_index
        if note_index < len(melody):
            freq, duration = melody[note_index]
            change_sound(freq, 20000)
            note_index += 1
            return duration
        return 0

    # MOVE 1: Big forward charge!
    duration = play_next_note()
    m.drive(25, 0)
    change_color((255,0,0))
    time.sleep_ms(duration)
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 2: Continue forward
    duration = play_next_note()
    m.drive(25, 0)
    change_color((255,50,0))
    time.sleep_ms(duration)
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 3: One more forward push
    duration = play_next_note()
    m.drive(25, 0)
    change_color((255,100,0))
    time.sleep_ms(duration)
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 4: Spin right
    duration = play_next_note()
    m.drive(0, math.radians(270))
    change_color((0,255,0))
    time.sleep_ms(duration + 100)
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 5: Arc move
    duration = play_next_note()
    m.drive(20, math.radians(90))
    change_color((0,255,100))
    time.sleep_ms(duration)
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 6: Straight forward
    duration = play_next_note()
    m.drive(25, 0)
    change_color((0,255,255))
    time.sleep_ms(duration)
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 7: Back arc
    duration = play_next_note()
    m.drive(15, -math.radians(90))
    change_color((0,150,255))
    time.sleep_ms(duration + 100)
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 8: Short forward burst
    duration = play_next_note()
    m.drive(20, math.radians(60))
    change_color((0,100,255))
    time.sleep_ms(duration)
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 9: Big hold with spin
    duration = play_next_note()
    m.drive(0, math.radians(540))
    change_color((100,0,255))
    time.sleep_ms(duration)
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 10: Forward burst
    duration = play_next_note()
    m.drive(25, 0)
    change_color((255,0,255))
    time.sleep_ms(duration)
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 11: Continue forward
    duration = play_next_note()
    m.drive(25, 0)
    change_color((255,0,200))
    time.sleep_ms(duration)
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 12: Forward again
    duration = play_next_note()
    m.drive(25, 0)
    change_color((255,0,150))
    time.sleep_ms(duration)
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 13: Spin left
    duration = play_next_note()
    m.drive(0, -math.radians(270))
    change_color((255,100,100))
    time.sleep_ms(duration + 100)
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 14: Arc right
    duration = play_next_note()
    m.drive(20, math.radians(90))
    change_color((255,150,0))
    time.sleep_ms(duration)
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 15: Side move
    duration = play_next_note()
    m.drive(15, -math.radians(120))
    change_color((200,200,0))
    time.sleep_ms(duration)
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 16: Back diagonal
    duration = play_next_note()
    m.drive(15, math.radians(60))
    change_color((100,255,100))
    time.sleep_ms(duration + 100)
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 17: Quick burst
    duration = play_next_note()
    m.drive(20, -math.radians(90))
    change_color((150,255,150))
    time.sleep_ms(duration)
    m.stop()
    time.sleep_ms(50)
    
    # MOVE 18: Grand finale - massive spin!
    duration = play_next_note()
    m.drive(0, math.radians(1080))
    for i in range(6):
        if i % 3 == 0:
            change_color((255,0,0))
        elif i % 3 == 1:
            change_color((0,255,0))
        else:
            change_color((0,0,255))
        time.sleep_ms(duration // 6)
    m.stop()
    
    # Quick celebration moves with remaining energy!
    change_sound(523, 15000)  # C
    m.drive(15, 0)
    change_color((255,255,0))
    time.sleep_ms(200)
    m.drive(-15, 0)
    change_color((0,255,255))
    time.sleep_ms(200)
    m.drive(15, 0)
    change_color((255,0,255))
    time.sleep_ms(200)
    m.stop()
    
    # Lights off, buzzer off
    change_color((0,0,0))
    buzzer.duty_u16(0)
    time.sleep_ms(500)
    buzzer.duty_u16(0)
    time.sleep_ms(500)
