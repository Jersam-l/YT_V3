import numpy as np
import matplotlib.pyplot as plt

c=1
n=250
v=0.05

x=np.linspace(0,c,n)
xv=np.linspace(1,c,n)
y=np.linspace(0,v,n)
yd=np.linspace(0,-v,n)
yv=np.linspace(v,-v,n)

line_x=np.concatenate((x[1:],xv[1:]))
line_y=np.concatenate((y[1:],yv[1:]))
line_y=np.concatenate((line_y,yd[::-1]))
line_x=np.concatenate((line_x,x[::-1]))

plt.figure(figsize=(1.5,1.5))
plt.plot(line_x,line_y)
plt.grid(True)
plt.axis('equal')
plt.show()