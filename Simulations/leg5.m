function [error,x,y,z]=leg5(l1,L2,L3,a)

x=l1(1)-L2*cos(a)*sin(50/180*pi);
y=l1(2)+L2*cos(a)*cos(50/180*pi);
z=l1(3)-L2*sin(a);

error=abs(L3-sqrt(x^2+y^2+z^2));

end