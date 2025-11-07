from machine import Pin
import time

class LineReader:
    def __init__(self, pins, positions):
        self.pins = pins
        self.positions = positions
        self.offset = 0.0
    
    def update(self):
        samples = 40
        delay_us = 15
        # charge capacitance
        for pin in self.pins:
            pin.init(Pin.OUT, value=1)
        time.sleep_us(10)
            # change to input
        for pin in self.pins:
            pin.init(Pin.IN, pull = None)
        counts = [0] * len(self.pins)

        for i in range(samples):
            # wait one sample period
            time.sleep_us(delay_us)
            # count the number of 1's
            for j, p in enumerate(self.pins):
                counts[j] += p.value()   
        # the pulse width is the number of 1's 
        # detected times the delay
        decay_times = [c * delay_us for c in counts]

        minimum = min(decay_times)
        total = sum(decay_times) - minimum * 6
        for i in range(len(decay_times)):
            decay_times[i] = decay_times[i] - minimum
            if total != 0:
                decay_times[i] = decay_times[i] / total
            else:
                decay_times[i] = 0
        final_sum = 0
        for i in range(len(self.pins)):  
            final_sum += decay_times[i] * self.positions[i]
        self.offset = final_sum
