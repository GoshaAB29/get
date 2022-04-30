import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
comp = 4
troyka = 17
data = []

GPIO.setmode(GPIO.BCM)

GPIO.setup(dac,GPIO.OUT)
GPIO.setup(leds,GPIO.OUT, initial = 0)
GPIO.setup(troyka, GPIO.OUT, initial = 0)
GPIO.setup(comp, GPIO.IN)

def dec2bin(value):                                       #перевод десятичного целого числа в двоичное (в виде списка);
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def bin2dec(list):                                        #перевод числа из 2 в 10;
    value = 0
    weight = 128
    for i in range (0,8):
        val = val + weight * list[i]
        weight = weight / 2
    return val

def adc():                                                #треугольный сигнал
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

    while (value <= 0.97 * 255):                                               #начало процесса зарядки конденсатора (до 97%)
        value = adc()
        data.append(val)

        print(str(3.3 * value/256) + " V")
        GPIO.output (leds, dec2bin(value))
    
    end_charging_t = time.time()
    charge_t = end_charging_t - start_t

    GPIO.output (troyka, 0)

    value = 255
    while (value >= 0.02 * 255):                                              #начало процесса разрядки конденсатора (до 2%)
        value = adc()
        data.append(value)

        print(str(3.3 * value/256) + " V")

        GPIO.output(leds, dec2bin(val))

    end_discharging_t = time.time()
    end_t = end_discharging_t - start_t

finally:                                                                          #сброс настроек
    GPIO.output(dac, 0)
    GPIO.output (troyka, 0)
    GPIO.cleanup()
    GPIO.cleanup(dac)
    GPIO.cleanup(leds)

plt.plot(data)                                                                    #график зависимости напряжения от времени
plt.show()

print("Общая продолжительность эксперимента: {} c".format(experiment_time))
print("Период одного измерения: {} c".format(0.01))
print("Средняя частота дискретизации: {} Гц".format(100))
print("Шаг квантования АЦП: {}".format(3.3/256))

data_str = [str(item) for item in data]

with open ("data.txt", "w") as data_outfile:                                        #запись напряжения;
        data_outfile.write("\n".join(data_str))

with open ("settings.txt", "w") as settings_outfile:                                #запись времени, периода, частоты и шага квантования;
        settings_outfile.write("Общая продолжительность эксперимента: {} c".format(experiment_time))
        settings_outfile.write("Период одного измерения: {} c".format(0.01))
        settings_outfile.write("Средняя частота дискретизации: {} Гц".format(100))
        settings_outfile.write("Шаг квантования АЦП: {}".format(3.3/256))
        
