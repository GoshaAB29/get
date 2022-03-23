import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
i = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

def dec2bin(value):
    return [int(bin) for bin in bin(value)[2:].zfill(8)]

def dec2dac(value):
    signal = dec2bin(value)
    GPIO.output(dac, signal)

try:
    period = 3

    while True:
        for i in range(255):
            dec2dac(i)
            time.sleep(period/510)
        i = 255

        while i >= 0:
            dec2dac(i)
            time.sleep(period/510)
            i = i - 1
    
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()