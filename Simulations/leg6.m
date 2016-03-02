function [error,x,y,z,a]=leg6(l1,L2,L3)


amin=0;
amax=pi/2;
tol=0.00001;
iter=0;
error=10;
a=amin;
while abs(error)>tol && iter<150
    
   
x=l1(1)+L2*cos(a)*sin(9*pi/6);
y=l1(2)-L2*cos(a)*cos(9*pi/6);
z=l1(3)-L2*sin(a);      
error=L3-sqrt(x^2+y^2+z^2);

if error>0
    amax=a;
    
else
    amin=a;
end

iter=iter+1;
a=amin+(-amin+amax)/2;   
end