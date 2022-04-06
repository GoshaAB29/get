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
    val = 0
    for i in range (7, -1, -1):

        fc = 2**i
        val = val + fc

        GPIO.output (dac, dec2bin (val))
        time.sleep (0.008)
        if GPIO.input(comp) == 0:
           val = val - fc

    print ("ADC dec = ", val)
    return val


try:
    while True:
        x = 3.3/256 * adc()
        print ("U = ", x)


finally:
    GPIO.output(dac, 0)
    GPIO.output (troyka, 0)
    GPIO.cleanup()