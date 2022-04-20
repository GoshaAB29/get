import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
comp = 4
troyka = 17
data = []

GPIO.setmode (GPIO.BCM)

GPIO.setup (leds, GPIO.OUT)
GPIO.setup (dac, GPIO.OUT)
GPIO.setup (troyka, GPIO.OUT)
GPIO.setup (comp, GPIO.IN)

def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def bin2dec(list):
    value = 0
    weight = 128
    for i in range (0,8):
        val = val + weight * list[i]
        weight = weight / 2
    return val

def adc():
    list = [0] * 8
    for j in range (0,8)
        list[j] = 1
        GPIO.output(dac, list)

        time.sleep (0.2)

        if (GPIO.input(comp) == 0):
            list[j] = 0    
    return bin2dec(list)

try:
    start_t = time.time()
    GPIO.output(17, 1)
    value = 0

    while (value <= 0.97 * 255):
        value = adc()
        data.append(val)

        print(str(3.3 * value/256) + " V")
        GPIO.output (leds, dec2bin(value))
    
    end_charging_t = time.time()
    charge_t = end_charging_t - start_t

    GPIO.output (17, 0)

    value = 255
    while (value >= 0.02 * 255):
        value = adc()
        data.append(value)

        print(str(3.3 * value/256) + " V")

        GPIO.output(leds, dec2bin(val))

    end_discharging_t = time.time()
    end_t = end_discharging_t - start_t

finally:
    GPIO.output(dac, 0)
    GPIO.output (troyka, 0)
    GPIO.cleanup()
    