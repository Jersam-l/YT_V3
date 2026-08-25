import numpy as np
import matplotlib.pyplot as plt

c=1.0 #chord length
n=1000 #number of points

# x coordinate
x=np.linspace(0,c,n)
m=0.02   #chamber
p=0.4    #position of the chamber
t=0.12  #thickness

xu=np.zeros(n)
yu=np.zeros(n)
xl=np.zeros(n)
yl=np.zeros(n)
yc=np.zeros(n)
yt=np.zeros(n)
theta=np.zeros(n)

for i,xi in enumerate(x):
	yt[i]=5*t*(0.2969*np.sqrt(xi)-0.1260*xi-0.3516*xi**2+0.2843*xi**3-0.1036*xi**4)

	if xi <= p*c:
		yc[i]=(m/(p**2))*(2*p*xi-xi**2)
		dyc_dx=(m/p**2)*(2*p-2*xi)
	else:
		yc[i]=(m/((1-p)**2))*((1-2*p)+2*p*xi-xi**2)
		dyc_dx=(m/(1-p)**2)*(2*p-2*xi)
	theta[i]=np.arctan(dyc_dx)

xu=x-yt*np.sin(theta)
yu=yc+yt*np.cos(theta)
xl=x+yt*np.sin(theta)
yl=yc-yt*np.cos(theta)

boundary_x=np.concatenate((xu[::-1],xl[1:]))
boundary_y=np.concatenate((yu[::-1],yl[1:]))

plt.figure(figsize=(10,4))
plt.plot(boundary_x,boundary_y,label="airfoil surface")
plt.plot(x,yc,"--",label="chamber line")
plt.grid(True)
plt.axis('equal')
plt.legend()
plt.show()	

