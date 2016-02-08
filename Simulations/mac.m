function [error]=mac(oq,op,pq,a)

vpq=[oq(1)-op*cos(a)*(-0.5),oq(2)-op*sin(a)*sqrt(3)/2,oq(3)-op*sin(a)];

error=sqrt(vpq(1)^2+vpq(2)^2+vpq(3)^2)-pq;

end