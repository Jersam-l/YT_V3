import numpy as np
import matplotlib.pyplot as plt

degrees=np.linspace(90,270,400)
theta=np.deg2rad(degrees)
xc=0
yc=0
r=5

x=xc+r*np.cos(theta)
y=yc+r*np.sin(theta)


plt.figure(figsize=(10,6))
plt.plot(x,y)
plt.grid(True)
plt.axis('equal')
plt.show()
