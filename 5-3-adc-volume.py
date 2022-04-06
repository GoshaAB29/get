import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
comp = 4
troyka = 17

GPIO.setmode (GPIO.BCM)

GPIO.setup (leds, GPIO.OUT)
GPIO.setup (dac, GPIO.OUT)
GPIO.setup (troyka, GPIO.OUT, initial = 1)
GPIO.setup (comp, GPIO.IN)

def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def adc ():

    val = 0
    for i in range (7, -1, -1):

        fc = 2**i
        val = val + fc
        signal = num2dac (val)
        GPIO.output (dac, dec2bin (val))
        time.sleep (0.01)

        if GPIO.input(comp) == 0:
           val = val - fc
        V = val * 3.3 / 256

    GPIO.output(leds, dec2bin(val))
    print("ADC dec = ", val, "; V = ", V)
    return val

def num2dac(value):
    signal = dec2bin(value)
    GPIO.output(dac, signal)
    return signal

def dec2dac(value):
    signal = dec2bin(value)
    GPIO.output(dac, signal)
        
try:
    while True:
        adc ()

finally:
    GPIO.output(dac, 0)
    GPIO.output (troyka, 0)
    GPIO.cleanup()
    