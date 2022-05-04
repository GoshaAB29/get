import numpy as np
import matplotlib.pyplot as plt

plt.minorticks_on()
plt.grid (True, "minor", ls = ":", c = 'grey')


volt = np.loadtxt ('data.txt')
volt *= 3.3/255
settings = np.loadtxt ('settings.txt')

charge = settings[2]
finish = settings[3]
dt = settings[0]
dv = settings[1]

time = np.linspace (0, finish, len(volt))

x_axes = np.linspace (0, finish, 10)
y_axes = np.linspace(0, volt.max(), 10)

plt.ylim([0, volt.max() * 1.1])
plt.xlim([0, finish])
plt.grid(which='major', color='blue', linestyle='-', linewidth=0.5)
plt.grid(which='minor', color='grey', linestyle='-', linewidth=0.25)
plt.plot(time, volt, c='orange', linewidth=0.75, label = 'V(t)')
plt.axvline(charge, linestyle=':', c='green', linewidth=0.75, label = "start discharging")
    
plt.text(charge + 5, volt.max() - 0.5, "charge time: {:.2f} с".format(charge))
plt.text(charge + 5, volt.max() - 0.6, "discharge time:  {:.2f} с".format(finish - charge))
plt.xlabel(r'$Time$, $c$',    wrap=True)
plt.ylabel(r'Voltage, $V$', wrap=True)
plt.scatter (charge, volt.max(), c='green')
plt.scatter (0, 0, c='red')
plt.scatter (10, 2, c='red')
plt.scatter (20, 2.62, c='red')
plt.scatter (30, 1, c='red')
plt.scatter (40, 0.36, c='red')
plt.legend()
plt.title('Charging and discharging process in RC circuit', wrap=True)
plt.savefig ('graph.svg')
plt.show()