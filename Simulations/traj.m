function [length1,L1,length2,L2,length3,L3 ,length4,L4 ,length5,L5 ,length6,L6,Bx,By,Bz,Tx,Ty,Tz] = traj(x2,y2,z2,ax,ay,az )
%traj(xdesired(i),ydesired(i),1+zdesired(i),anglex(i)+axtilt(i),angley(i)+aytilt(i),anglez(i)); 

%Define radii of Top and Base (meters)
r1 = 0.402;
r2 = 0.265;

%Establish Angles for the points on the hexagon(base) and the triangle(top)
%The right edge of the triangle is deemed to be 0. The hex begins at +/- 30
%degrees
hex_angles = [-pi/6:pi/3:9*pi/6];
tri_angles = [0,2*pi/3,4*pi/3];

%Establish the points of the base
Bx = r1.*cos(hex_angles);
By = r1.*sin(hex_angles);
Bz = zeros(size(hex_angles));

%Establish the points of the top
Tx = r2.*cos(tri_angles);
Ty = r2.*sin(tri_angles);
Tz = zeros(size(tri_angles));

%Initialize the platform location
P=[x2; y2; z2];

%Initialize variables to work with the rest of Andy's code below
T1 = [Tx(1);Ty(1);Tz(1)];
T2 = [Tx(2);Ty(2);Tz(2)];
T3 = [Tx(3);Ty(3);Tz(3)];

B1 = -1.*[Bx(1);By(1);Bz(1)];
B2 = -1.*[Bx(2);By(2);Bz(2)];
B3 = -1.*[Bx(3);By(3);Bz(3)];
B4 = -1.*[Bx(4);By(4);Bz(4)];
B5 = -1.*[Bx(5);By(5);Bz(5)];
B6 = -1.*[Bx(6);By(6);Bz(6)];

ax=ax/180*pi;
ay=ay/180*pi;
az=az/180*pi;

Rx=[1 0 0; 0 cos(ax) -sin(ax); 0 sin(ax) cos(ax)];
Ry=[cos(ay) 0 sin(ay); 0 1 0; -sin(ay) 0 cos(ay)];
Rz=[cos(az) -sin(az) 0; sin(az) cos(az) 0; 0 0 1];

T1=Rx*T1;
T1=Ry*T1;
T1=Rz*T1;

T2=Rx*T2;
T2=Ry*T2;
T2=Rz*T2;

T3=Rx*T3;
T3=Ry*T3;
T3=Rz*T3;

L1=B1+P+T1;
L2=B2+P+T1;
L3=B3+P+T2;
L4=B4+P+T2;
L5=B5+P+T3;
L6=B6+P+T3;

% T4=Rx*T4;
% T4=Ry*T4;
% T4=Rz*T4;

% T5=Rx*T5;
% T5=Ry*T5;
% T5=Rz*T5;

% T6=Rx*T6;
% T6=Ry*T6;
% T6=Rz*T6;

length1=sqrt(L1(1)^2+L1(2)^2+L1(3)^2);
length2=sqrt(L2(1)^2+L2(2)^2+L2(3)^2);
length3=sqrt(L3(1)^2+L3(2)^2+L3(3)^2);
length4=sqrt(L4(1)^2+L4(2)^2+L4(3)^2);
length5=sqrt(L5(1)^2+L5(2)^2+L5(3)^2);
length6=sqrt(L6(1)^2+L6(2)^2+L6(3)^2);

end

