function [error,x,y,z]=leg1(l1,L2,L3,a)

x=l1(1)+L2*cos(a)*sin(-pi/6);
y=l1(2)-L2*cos(a)*cos(-pi/6);
z=l1(3)-L2*sin(a);



error=abs(L3-sqrt(x^2+y^2+z^2));

end