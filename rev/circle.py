import numpy as np
import matplotlib.pyplot as plt

deg =np.linspace(90,270,500)
# deg =np.linspace(90,-90,500)
theta=np.deg2rad(deg)

xc=0
yc=0
r=3

x=xc+r*np.cos(theta)
y=yc+r*np.sin(theta)

plt.figure(figsize=(3.5,3.5))
plt.plot(x,y)
plt.grid(True)
plt.axis('equal')
plt.show()