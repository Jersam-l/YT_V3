import numpy as np
import matplotlib.pyplot as plt

chord=1
n=250
v=0.05
max_camber=0.05
position_max_camber=0.4
line_x=np.linspace(0,chord,n)
line_y=np.zeros(n)

for i in range(n):
    if line_x[i]<position_max_camber:
        line_y[i]=max_camber*(line_x[i]/position_max_camber)
    else:
        line_y[i]=max_camber*((chord-line_x[i])/(chord-position_max_camber))

plt.figure(figsize=(1.5,1.5))
plt.plot(line_x,line_y)
plt.grid(True)
plt.axis('equal')
plt.show()