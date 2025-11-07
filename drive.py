import machine
from machine import Pin, PWM
import time
import math
import neopixel


class MotorDriver:
    def __init__(self, pinA, pinB, freq=8000):
        self.MA = PWM(Pin(pinA))
        self.MB = PWM(Pin(pinB))
        self.MA.freq(freq)
        self.MB.freq(freq)

    def set_pwm(self, PWM_val, direction):
        if direction >= 0:
            self.MA.duty_u16(int(PWM_val))
            self.MB.duty_u16(0)
        else:
            self.MA.duty_u16(0)
            self.MB.duty_u16(int(PWM_val))

    def stop(self):
        self.MA.duty_u16(0)
        self.MB.duty_u16(0)

class Ultrasound():
    def __init__(self, trigger, echo, timeout = 1e6):
        self.t = trigger
        self.e = echo
        self.timeout = timeout
    def measure(self):
        self.t.low()
        time.sleep_us(2)
        self.t.high()
        time.sleep_us(15)
        self.t.low()
        start_time = time.ticks_us()
        while self.e.value() == 0:
            signaloff = time.ticks_us()
            if time.ticks_diff(signaloff,start_time) >= self.timeout:
                raise TimeoutError
            
        start_time = time.ticks_us()
        while self.e.value() == 1:
            signalon = time.ticks_us()
            if time.ticks_diff(signalon,start_time) >= self.timeout:
                raise TimeoutError
        timepassed = signalon - signaloff

        return ((timepassed/1000) * 16.7) + 1.19

class Drive:
    def __init__(self, left_pins, right_pins, L=13, bias=-0.07):
        self.L = L
        self.bias = bias

        self.left_bias = 1.0 - bias / 2
        self.right_bias = 1.0 + bias / 2

        self.left_motor = MotorDriver(*left_pins)
        self.right_motor = MotorDriver(*right_pins)

    def drive(self, speed, omega):
        L = self.L

        v_L = (speed) - ((-omega * L) / 2)
        v_R = (speed) + ((-omega * L) / 2)

        PWM_L = abs(1080 * v_L) + 6152
        PWM_R = abs(1080 * v_R) + 6152

        PWM_L *= self.left_bias
        PWM_R *= self.right_bias

        self.left_motor.set_pwm(PWM_L, v_L)
        self.right_motor.set_pwm(PWM_R, v_R)

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()


class Feedback:
    def __init__(self, pixel_pin=18, buzzer_pin=22, num_pixels=2):
        self.np = neopixel.NeoPixel(Pin(pixel_pin), num_pixels)
        self.buzzer = PWM(Pin(buzzer_pin))
        self.buzzer.duty_u16(0)

    def set_feedback(self, distance):
        if distance < 5:
            color = (255, 0, 0)   # Red
            freq = 1500
            duty = 20000
        elif distance < 15:
            color = (255, 150, 0) # Orange
            freq = 1000
            duty = 12000
        elif distance < 30:
            color = (0, 255, 0)   # Green
            freq = 700
            duty = 6000
        else:
            color = (0, 0, 255)   # Blue
            freq = 0
            duty = 0

        for i in range(len(self.np)):
            self.np[i] = color
        self.np.write()

        if freq > 0:
            self.buzzer.freq(freq)
            self.buzzer.duty_u16(duty)
        else:
            self.buzzer.duty_u16(0)

    def clear(self):
        for i in range(len(self.np)):
            self.np[i] = (0, 0, 0)
        self.np.write()
        self.buzzer.duty_u16(0)

if __name__ == "__main__":
    robot = Drive(left_pins=(8, 9), right_pins=(10, 11))
    sensor = Ultrasound(trigger=Pin(28, Pin.OUT), echo=Pin(7, Pin.IN))
    feedback = Feedback(pixel_pin=18, buzzer_pin=22, num_pixels=2)

    def run_test(name, speed, omega, duration_ms):
        start = time.ticks_ms()
        robot.drive(speed, omega)

        try:
            while time.ticks_diff(time.ticks_ms(), start) < duration_ms:
                try:
                    dist = sensor.measure()
                    feedback.set_feedback(dist)
                except TimeoutError:
                    pass
                time.sleep(0.01)
        finally:
            robot.stop()
            feedback.clear()
            time.sleep_ms(500)

    # --- Movement tests ---
    run_test("STRAIGHT", 20, 0, 500)
    run_test("REVERSE", -20, 0, 500)
    run_test("RIGHT TURN", 20, math.radians(180), 500)
    run_test("LEFT TURN", 20, -math.radians(180), 500)
    run_test("ROTATE 360", 0, math.radians(360), 1000)
