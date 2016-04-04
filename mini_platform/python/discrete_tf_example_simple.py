from numpy import *
from scipy.signal import *
from matplotlib.pyplot import *



#let's make a variable to keep track of current and old inputs.

N = 1200
dt = 0.1

u_meas = ones(N)
y_meas = zeros(N)
t = arange(0,N*dt,dt)

sys = lti([1],[1,1,1])

(tout,yout,xout) = lsim(sys,u_meas,t,X0=0)

for index in range(2,N):
    y_meas[index] = 1.9*y_meas[index-1] - .905*y_meas[index-2] + 0.004833*u_meas[index-1] + .004775*u_meas[index-2]#calculate the value of y RIGHT y_now


figure()
plot(t,y_meas,t,yout)
show()