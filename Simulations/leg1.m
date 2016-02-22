function [error,x,y,z]=leg1(L1,L2,L3,a)

x=L1(1)+L2*cos(a)*sin(-pi/6);
y=L1(2)-L2*cos(a)*cos(-pi/6);
z=L1(3)-L2*sin(a);



error=abs(L3-sqrt(x^2+y^2+z^2));

end