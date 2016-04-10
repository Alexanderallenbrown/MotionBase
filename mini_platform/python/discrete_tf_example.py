from numpy import *
from matplotlib.pyplot import *



#let's make a variable to keep track of current and old inputs.



u_meas = zeros(3)
y_meas = zeros(3)

y_output = array([])
t_output = array([])
u_now = 1
dt = .1
t_now = 0

for index in range(0,120):
    t_output = append(t_output,t_now)
    y_now = 1.9*y_meas[1] - .905*y_meas[0] + 0.004833*u_meas[1] + .004775*u_meas[0]#calculate the value of y RIGHT y_now
    y_output = append(y_output,y_now)
    y_meas = array([y_meas[1] , y_meas[2], y_now])
    u_meas = append(u_meas[1:],u_now)
    t_now+=dt


figure()
plot(t_output,y_output)

figure()
plot(t_output,)
show()