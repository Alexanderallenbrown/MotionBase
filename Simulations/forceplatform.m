function [F] = forceplatform(m, J, Rpq1, Rpq2, Rpq3, Rpq4, Rpq5,Rpq6, r1, r2, r3, acc, theta)
%inputs:
%   for point r(i) on top platform:
%                    Rpq(i)=(x,y,z)      vector of the arm
%                       
%   requests:        acc=(x,y,z)         acceleration vector
%                    theta=(x,y,z)       angle
%                       
%   properties:      m                   mass
%                    J                   inertia
%

e1 = Rpq1/norm(Rpq1);
e2 = Rpq2/norm(Rpq2);
e3 = Rpq3/norm(Rpq3);
e4 = Rpq4/norm(Rpq4);
e5 = Rpq5/norm(Rpq5);
e6 = Rpq6/norm(Rpq6);       % e is the unit vector in the direction of the force

M1 = cross(r1, e1);
M2 = cross(r1, e2);
M3 = cross(r2, e3);
M4 = cross(r2, e4);
M5 = cross(r3, e5);
M6 = cross(r3, e6);       % M is the unit vector giving the direction of the moment

A = [e1(1), e2(1), e3(1), e4(1), e5(1), e6(1);
    e1(2), e2(2), e3(2), e4(2), e5(2), e6(2);
    e1(3), e2(3), e3(3), e4(3), e5(3), e6(3);
    M1(1), M2(1), M3(1), M4(1), M5(1), M6(1); 
    M1(2), M2(2), M3(2), M4(2), M5(2), M6(2); 
    M1(3), M2(3), M3(3), M4(3), M5(3), M6(3)];

b = [m*acc(1);
    m*acc(2);
    m*acc(3);
    J*theta(1);
    J*theta(2);
    J*theta(3)];

F = A\b;






% [F]=forceplatform(ax,ay,az,alphax,alphay,alphaz,m,j,e1,e2,e3,e4,e5,e6,r1,r2,r3,r4,r5,r6)
% mage1=sqrt(e1(1)^2+e1(2)^2+e1(3)^2);
% mage2=sqrt(e2(1)^2+e2(2)^2+e2(3)^2);
% mage3=sqrt(e3(1)^2+e3(2)^2+e3(3)^2);
% mage4=sqrt(e4(1)^2+e4(2)^2+e4(3)^2);
% mage5=sqrt(e5(1)^2+e5(2)^2+e5(3)^2);
% mage6=sqrt(e6(1)^2+e6(2)^2+e6(3)^2);
% 
% a(1,1)=e1(1)/mage1;
% a(1,2)=e2(1)/mage2;
% a(1,3)=e3(1)/mage3;
% a(1,4)=e4(1)/mage4;
% a(1,5)=e5(1)/mage5;
% a(1,6)=e6(1)/mage6;
% 
% a(2,1)=e1(2)/mage1;
% a(2,2)=e2(2)/mage2;
% a(2,3)=e3(2)/mage3;
% a(2,4)=e4(2)/mage4;
% a(2,5)=e5(2)/mage5;
% a(2,6)=e6(2)/mage6;
% 
% a(3,1)=e1(3)/mage1;
% a(3,2)=e2(3)/mage2;
% a(3,3)=e3(3)/mage3;
% a(3,4)=e4(3)/mage4;
% a(3,5)=e5(3)/mage5;
% a(3,6)=e6(3)/mage6;
% 
% 
% a(4,1)=e1(3)/mage1*r1(2)-e1(2)/mage1*r1(3);
% a(4,2)=e2(3)/mage2*r2(2)-e2(2)/mage2*r2(3);
% a(4,3)=e3(3)/mage3*r3(2)-e3(2)/mage3*r3(3);
% a(4,4)=e4(3)/mage4*r4(2)-e4(2)/mage4*r4(3);
% a(4,5)=e5(3)/mage5*r5(2)-e5(2)/mage5*r5(3);
% a(4,6)=e6(3)/mage6*r6(2)-e6(2)/mage6*r6(3);
% 
% a(5,1)=e1(1)/mage1*r1(3)-e1(3)/mage1*r1(1);
% a(5,2)=e2(1)/mage2*r2(3)-e2(3)/mage2*r2(1);
% a(5,3)=e3(1)/mage3*r3(3)-e3(3)/mage3*r3(1);
% a(5,4)=e4(1)/mage4*r4(3)-e4(3)/mage4*r4(1);
% a(5,5)=e5(1)/mage5*r5(3)-e5(3)/mage5*r5(1);
% a(5,6)=e6(1)/mage6*r6(3)-e6(3)/mage6*r6(1);
% 
% a(6,1)=e1(2)/mage1*r1(1)-e1(1)/mage1*r1(2);
% a(6,2)=e2(2)/mage2*r2(1)-e2(1)/mage2*r2(2);
% a(6,3)=e3(2)/mage3*r3(1)-e3(1)/mage3*r3(2);
% a(6,4)=e4(2)/mage4*r4(1)-e4(1)/mage4*r4(2);
% a(6,5)=e5(2)/mage5*r5(1)-e5(1)/mage5*r5(2);
% a(6,6)=e6(2)/mage6*r6(1)-e6(1)/mage6*r6(2);
% 
% b=[m*ax;m*ay;m*az+m*9.8;j*alphax;j*alphay;j*alphaz];

end