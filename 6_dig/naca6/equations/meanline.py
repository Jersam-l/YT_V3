import numpy as np

def calculate_meanline(x_bar, a, cli):
    x_bar = np.asarray(x_bar, dtype=float)
    ym=np.zeros(len(x_bar))
    if not 0 < a <= 1:
        raise ValueError("The loading parameter 'a' must satisfy 0 < a <= 1.")
    # if a==1.0:
    #     for i, xi in enumerate(x_bar):
    #         if xi==0:
    #             term1=0.0
    #             term2=0.0
    #         elif xi== 1:
    #             term1 = 0.5 * xi**2 * np.log(xi) if xi > 0 else 0.0
    #             term2 = -0.5 * (1 - xi)**2 * np.log(1 - xi) if xi < 1 else 0.0
    #         else:
    #              term1 = 0.5 * xi**2 * np.log(xi)
    #              term2 = -0.5 * (1 - xi)**2 * np.log(1 - xi)
    #         term3 = 0.25 * (1 - xi)**2
    #         term4 = -0.25 * xi**2
    #         term5 = -0.75 * xi
    #         term6 = 0.25
    #         ym[i]=(cli/(2*np.pi)*(term1+term2+term3+term4+term5+term6))
    #     return ym
            
    else:
        g=-((a**2*((1/2)*np.log(a)-(1/4))+(1/4))/(1-a))
        h=(((1/2)*(1-a)**2*np.log(1-a)-(1/4)*(1-a)**2)/(1-a))+g
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
        return ym