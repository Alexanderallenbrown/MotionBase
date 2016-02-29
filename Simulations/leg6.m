function [error,x,y,z,a]=leg6(l1,L2,L3)


amin=0;
amax=pi;
tol=0.00001;
iter=0;
error=10;

while abs(error)>tol && iter<10
    
a=(amin+amax)/2;    
x=l1(1)+L2*cos(a)*sin(9*pi/6);
y=l1(2)-L2*cos(a)*cos(9*pi/6);
z=l1(3)-L2*sin(a);      
error=L3-sqrt(x^2+y^2+z^2);

if error>0
    amax=(amin+amax)/2;
    
else
    amin=(amin+amax)/2;
end

iter=iter+1;

end