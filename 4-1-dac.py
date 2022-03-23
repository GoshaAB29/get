import RPi.GPIO as GPIO

dac = [26, 19, 13, 6, 5, 11, 9, 10]

GPIO.setmode(GPIO.BCM)   
GPIO.setup(dac, GPIO.OUT)


def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

try:
    while True:
        
        X = input("enter number in [0;255]: ")

        if X == 'q': 
            break

        if X.isdigit():
            
            if float(X) % 1 != 0:
                print ("error, enter integer number")
                continue
            elif int(X) > 255:
               print ("error, enter number < 256 ")
               continue

            elif int(X) < 0:
                print ("error, enter number > 0")
                continue
        
            X = int(X)
            GPIO.output(dac, dec2bin(X))
            print("U = ", X*3.3/256, " V")
        else:
            print ("error, enter number")

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()

