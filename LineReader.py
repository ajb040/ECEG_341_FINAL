from machine import Pin
import time

def reflectance_sample(pins, samples, delay_us):
    # charge capacitance
    for pin in pins:
        pin.init(Pin.OUT, value=1)
    time.sleep_us(10)
        # change to input
    for pin in pins:
        pin.init(Pin.IN, pull = None)
    counts = [0] * len(pins)

    for i in range(samples):
        # wait one sample period
        time.sleep_us(delay_us)
        # count the number of 1's
        for j, p in enumerate(pins):
            counts[j] += p.value()   
    # the pulse width is the number of 1's 
    # detected times the delay
    decay_times = [c * delay_us for c in counts]
    return decay_times

if __name__=="__main__":   
    pins = [Pin(5),Pin(4),Pin(3),Pin(2),Pin(1),Pin(0)]
    pos=[-20,-12,-4, 4, 12, 20]
    while True:        
        d = reflectance_sample(pins, 
                samples = 40, delay_us = 15)
        minimum = min(d)
        total = sum(d) - minimum * 6
        for i in range(len(d)):
            d[i] = d[i] - minimum
            if total != 0:
                d[i] = d[i] / total
            else:
                d[i] = 0
        final_sum = 0
        for i in range(len(pins)):  
            final_sum += d[i] * pos[i]
            
        print(f"Offset: {final_sum}")
        time.sleep(0.5)
