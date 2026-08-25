import numpy as np
import matplotlib.pyplot as plt
#The designation can be interpreted as:    #EXAMPLE=     naca 66(2)-015
# FIRST(6) tells us thet it is a 6 series airfoil
# SECOND(6) tells us the minimum  pressure region [a]
# third(2) tells us the design lift coefficient [cli]
# fourth(015) tells us that  the minimum thickness is 15% of the chord length (t/c=0.15) [t_dc]

naca6=(str(input("Enter the 6 digits of the NACA series whose coordinates were needed :")))
if len(naca6)!=6:
    print("Please enter a valid 6 digit NACA series bruh")
    exit()
chord=float(input("Enter the required chord length :"))
n=int(input("Enter the number of points needed for the coordinates (whole number) :"))

a=(int(naca6[1]))/10
cli=(int(naca6[2]))/10
t_dc=(int(naca6[3:]))/100 
# x_bar=x/chord so x=x_bar*chord
x_bar=np.linspace(0,1,n)
x=x_bar*chord
ym=np.zeros(n)
yt=np.zeros(n)
yu=np.zeros(n)
yl=np.zeros(n)
#constants
g=-((a**2*((1/2)*np.log(a)-(1/4))+(1/4))/(1-a))
h=(((1/2)*(1-a)**2*np.log(1-a)-(1/4)*(1-a)**2)/(1-a))+g
#formulas [mean line]
mk=cli/(2*np.pi*(a+1))
for i, xi in enumerate(x_bar):
    if xi==0:
        mt1=(1/2)*a**2*np.log(a)
        l=0
        mt2=0
    elif xi==a:
        mt1=0
        mt2=-((1/2)*(1-xi)**2*np.log(1-xi))
        l=-xi*np.log(xi)
    elif xi==1:
        mt1=(1/2)*(a-xi)**2*np.log(np.abs(a-xi))
        l=0
        mt2=0
    else:
        mt1=(1/2)*(a-xi)**2*np.log(np.abs(a-xi))
        mt2=-((1/2)*(1-xi)**2*np.log(1-xi))
        l=-xi*np.log(xi)
    mt3=(1/4)*(1-xi)**2
    mt4=-((1/4)*(a-xi)**2)
    mb1=mt1+mt2+mt3+mt4
    mb2=mb1/(1-a)
    # l=-x_bar*np.log(x_bar)
    mb3=l+g-h*xi
    mb4=mb2+mb3
    ym[i]=mk*mb4
#------------------[end of mean line]>>>>>[thickness distribution]
xt_data = np.array([
    0.0000, 0.0050, 0.0075, 0.0125, 0.0250,
    0.0500, 0.0750, 0.1000, 0.1500, 0.2000,
    0.2500, 0.3000, 0.3500, 0.4000, 0.4500,
    0.5000, 0.5500, 0.6000, 0.6500, 0.7000,
    0.7500, 0.8000, 0.8500, 0.9000, 0.9500,
    1.0000
])

yt_data = np.array([
    0.0000, 0.011157, 0.013386, 0.016666, 0.022326,
    0.030980, 0.037831, 0.043558, 0.052863, 0.059963,
    0.065444, 0.069573, 0.072494, 0.074291, 0.074979,
    0.074531, 0.072853, 0.069614, 0.063846, 0.055686,
    0.046263, 0.035911, 0.025222, 0.014839, 0.005635,
    0.0000
])
for i,xi in enumerate(x_bar):
    yt[i]=chord*np.interp(xi, xt_data, yt_data)
    yu[i]=ym[i]+yt[i]
    yl[i]=ym[i]-yt[i]





# plt.figure(figsize=(2.5,2.5))
plt.plot(x,ym)
plt.plot(x,yt,'--')
plt.plot(x,yu)
plt.plot(x,yl)
plt.axis('equal')
plt.grid(True)
plt.show()