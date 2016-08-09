from numpy import *
from matplotlib.pyplot import *

# A Dugoff Tire model implementation in python/numpy
#Alexander Brown, Ph.D.
# brownaa@lafayette.edu

class DugoffTire:
    """ This python class implements the Dugoff tire model based on friction coefficients, cornering stiffnesses. 
    Forces are applied in same sign as slip angle, so be aware of this when you implement.
    Units are SI """
    def __init__(self,Ca=100000,Ck=1000000,mu=0.8,Fz = 4500):
        """ init(self,Ca=100000,Ck=1000000,mu=0.8,Fz=4500):
            Ca is cornering stiffness in Nm/rad
            Ck is longitudinal stiffness
            mu is the (single) Dugoff friction coefficient
            Fz is an initial vertical load, guessing 50/50 even weight on a 4000 lb car
        """
        self.Ca = Ca
        self.Ck = Ck
        self.mu = mu
        self.Fz = Fz



    def calcSlipxy(self,Vr,Vx,Vy,Ty):
        """ calcSlipxy(self,Vr,Vx,Vy)
        returns: kappa, alpha
        kappa is longitudinal slip fraction
        alpha is lateral slip angle
        takes into account whether cornering or braking. SAE axis system on wheel center. z down, x forward, y right.

        Vr is the "omega*r_effective" velocity where omega is the rotational velocity of the wheel. positive is forward velocity.
        Therefore, if Vr>Vx, it means that the tire is accelerating. If Vr<Vx, it is braking. Thus, kappa>0 is acceleraing.

        driving (Ty>0 in SAE):
        k = -(1+k)*Vx/Vr 
        k(1+Vx/Vr) = -1
        k = -1/(1+Vx/Vr)
        braking (Ty<0 in SAE):
        k = -Vx/Vr for brake """
        if Ty>0:
            if Vx>0:
                kappa = -1/(1+Vx/(Vr))
                alpha = arctan((1+kappa)*-Vy/Vr)
            else:
                kappa=0
                alpha = 0
        else:
            
            if Vx>0:
                kappa = (Vr-Vx)/(Vx)
                alpha = arctan(-Vy/Vx)
            else:
                kappa=.1
                alpha = 0
        return kappa,alpha

    def calcFxFy(self,Fz,kappa,alpha,mu,Ca,Ck,Ty=0):
        """ calcFxFy(Fz,kappa,alpha,mu,Ca,Ck,Ty=0):
            returns: Fx,Fy 
            -Uses Dugoff tire model with isotropic friction (one mu)
            -Does not explicitly account for changes in cornering stiffness with load
            -Does not account for changes in Mu with load. You can program these in or maybe we'll add them.
            """
        if Ty<=0:
            sigy = tan(alpha)
            sigx = kappa
        else:
            sigy = tan(alpha)/(1+kappa)
            sigx = kappa/(1+kappa)

        Fxlin = Ck*sigx
        Fylin = Ca*sigy

        if sqrt(Fxlin**2+Fylin**2)<=(mu*Fz/2):
            Fx = Fxlin
            Fy = Fylin
        else:
            lam = (mu*Fz/2)/sqrt(Fxlin**2+Fylin**2) #lambda parameter
            Fx = Fxlin*(2*lam-lam**2)
            Fy = Fylin*(2*lam-lam**2)
        return Fx,Fy


def main():
    """ you have chosen to run the demo
        This just plots tire forces (Fy, Fz) for a range of slip angles and ratios.
    """
    #initialize tire model.
    tire = DugoffTire()
    #produce an array of slip values
    alpha = arange(0,20*pi/180,.001)
    #initialize output array of Fy values
    Fy_array = array([])
    #loop through and fill up array
    for ind in range(0,len(alpha)):
        Fx,Fy = tire.calcFxFy(4500,0,alpha[ind],0.9,100000,100000)
        Fy_array = append(Fy_array,Fy)
    #now do the same for longitudinal force
    kappa = arange(0,.2,.0001)
    #initialize output array of Fx values
    Fx_array = array([])
    #loop through and fill up array
    for ind in range(0,len(kappa)):
        Fx,Fy = tire.calcFxFy(4500,kappa[ind],0,0.9,100000,100000)
        Fx_array = append(Fx_array,Fx)

    figure(num=None,figsize=(12,6))
    title('Dugoff Tire Model')
    subplot(1,2,1)
    plot(alpha*180/pi,Fy_array,'k')
    grid()
    xlabel('slip angle (deg)')
    ylabel('Lateral Force (N)')
    subplot(1,2,2)
    plot(kappa,Fx_array,'k')
    xlabel('slip ratio')
    ylabel('Longitudinal Force (N)')
    grid()

    show()




if __name__ == '__main__':
    main()



