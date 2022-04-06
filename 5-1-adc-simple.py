import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17

GPIO.setmode (GPIO.BCM)
GPIO.setup (dac, GPIO.OUT)
GPIO.setup (troyka, GPIO.OUT, initial = 1)
GPIO.setup (comp, GPIO.IN)

def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def adc ():
    for i in range (256):
        GPIO.output (dac, dec2bin(i))
        time.sleep (0.008)
        input = GPIO.input (comp)
        
        if (input == 0):
            print ("ADC dec = ", i)
            return i


try:
    while True:
        x = 3.3/256 * adc()
        print ("U = ", x)


finally:
    GPIO.output(dac, 0)
    GPIO.output (troyka, 0)
    GPIO.cleanup()