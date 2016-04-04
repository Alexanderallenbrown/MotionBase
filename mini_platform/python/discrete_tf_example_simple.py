from numpy import *
from scipy.signal import *
from matplotlib.pyplot import *



#let's make a variable to keep track of current and old inputs.

N = 1200
dt = 0.1

u_meas = ones(N)
y_meas = zeros(N)
y_meas2 = zeros(N)
t = arange(0,N*dt,dt)

sys = lti([1],[1,1,1])
print sys
sysd = cont2discrete(([1],[1,1,1]),dt)
print sys,sysd

(tout,yout,xout) = lsim(sys,u_meas,t,X0=0)

for index in range(2,N):
    y_meas[index] = 1.895*y_meas[index-1] - .905*y_meas[index-2] + 0.004833*u_meas[index-1] + .004775*u_meas[index-2]#calculate the value of y RIGHT y_now
    #y_meas2now[index] = dlsim(sysd,array([u_meas[index-1],u_meas[index]]),array([t[index-1],t[index]]),x0=y_meas2[index-2])
    (tnow,youtnow,xoutnow) = lsim(sys,u_meas[index-2:index],t[index-2:index],X0=y_meas[index-1])
    y_meas2[index] = youtnow[-1]

figure()
plot(t,y_meas,t,yout,t,y_meas2)
show()