import numpy as np
import matplotlib.pyplot as plt

x = []
y = []

with open('F0000CH1.CSV', 'r', newline='') as file:
    next(file)
    for line in file:
        line_splitted = line.split(',')
        if float(line_splitted[3]) > 0.52 and float(line_splitted[4]) < 0.555:
            x.append(float(line_splitted[3]))
            y.append(float(line_splitted[4]))

y_top = max(y)
y_min = min(y)

# Gebruik index() om de bijbehorende x te vinden
x_top = x[y.index(y_top)]
x_min = x[y.index(y_min)]

print(x_top)
print(x_min)
print(y_top)
print(y_min)

a = (y_top - y_min) / (x_top - x_min)
print(a)
b = y_top - a * x_top

y_line = []
for i in x:
    y_line.append(a* i + b)

y_norm = []
for i in range (0, len(y_line)):
    y_norm.append(y_line[i] - y[i])


print(y_line)
plt.figure()  # was plt.figure zonder ()
plt.plot(x, y)
plt.plot(x, y_line)
plt.show()


plt.figure()
plt.plot(x, y_norm)
plt.xlim(0.525, 0.555)
plt.show()