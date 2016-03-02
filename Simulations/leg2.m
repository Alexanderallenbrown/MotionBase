function [error,x,y,z,a]=leg2(l1,L2,L3)

amin=0;
amax=pi/2;
tol=0.00001;
iter=0;
error=10;
a=amin;
while abs(error)>tol && iter<50
    
  
x=l1(1)+L2*cos(a)*sin(pi/6);
y=l1(2)-L2*cos(a)*cos(pi/6);
z=l1(3)-L2*sin(a);

error=L3-sqrt(x^2+y^2+z^2);
if error>0
    amax=a;
    
else
    amin=a;
end
a=amin+(-amin+amax)/2;  
iter=iter+1;

end