function [Length, Base, Platform] = traj(motion_desired, angle_desired, r1, r2)
%traj(xdesired(i),ydesired(i),1+zdesired(i),anglex(i)+axtilt(i),angley(i)+aytilt(i),anglez(i)); 
% Computes distance from motor shaft to connection point on top platform
%       Inputs:     motion_desired   vector(x,y,z) of the desired lateral motion
%                   angle_desired    vector(x,y,z) of the desired acceleration
%       Outputs:    L                matrix of vectors for legs 1-6
%                   length           matrix of length magnitudes
%                   Base             xyz location of base points
%                   Platform         xyz location of platform points

% Establish Angles for the points on the hexagon(base) and the triangle(top)
% The right edge of the triangle is deemed to be 0. The hex begins at +/- 30
% degrees
hex_angles = [-pi/6:pi/3:9*pi/6];
tri_angles = [0,2*pi/3,4*pi/3];

% Establish the points of the base
Bx = r1.*cos(hex_angles);
By = r1.*sin(hex_angles);
Bz = zeros(size(hex_angles));
B = [Bx, By, Bz];
Base = B';

% Establish the points of the platform
Tx = r2.*cos(tri_angles);
Ty = r2.*sin(tri_angles);
Tz = zeros(size(tri_angles));
T = [Tx, Ty, Tz];
Platform = T';

% Initialize the platform location
P=[motion_desired(1); motion_desired(2); motion_desired(3)];

% vectors from the middle of the top to the connection point (corners of triangle)
T1 = [Tx(1);Ty(1);Tz(1)];
T2 = [Tx(2);Ty(2);Tz(2)];
T3 = [Tx(3);Ty(3);Tz(3)];

% vectors from the motor shaft to the middle of the base (corners of hexagon)
B1 = -1.*[Bx(1);By(1);Bz(1)];
B2 = -1.*[Bx(2);By(2);Bz(2)];
B3 = -1.*[Bx(3);By(3);Bz(3)];
B4 = -1.*[Bx(4);By(4);Bz(4)];
B5 = -1.*[Bx(5);By(5);Bz(5)];
B6 = -1.*[Bx(6);By(6);Bz(6)];

% rotation matrices
Rx=[1 0 0; 0 cos(angle_desired(1)) -sin(angle_desired(1)); 0 sin(angle_desired(1)) cos(angle_desired(1))];
Ry=[cos(angle_desired(2)) 0 sin(angle_desired(2)); 0 1 0; -sin(angle_desired(2)) 0 cos(angle_desired(2))];
Rz=[cos(angle_desired(3)) -sin(angle_desired(3)) 0; sin(angle_desired(3)) cos(angle_desired(3)) 0; 0 0 1];

% rotate the top vectors using rotation matrices, z y x order because yaw
%   angle will probably be the largest
T1=Rz*T1;
T1=Ry*T1;
T1=Rx*T1;

T2=Rz*T2;
T2=Ry*T2;
T2=Rx*T2;

T3=Rz*T3;
T3=Ry*T3;
T3=Rx*T3;

% compute vector from motor shaft to triangle points
L1=B1+P+T1;
L2=B2+P+T1;
L3=B3+P+T2;
L4=B4+P+T2;
L5=B5+P+T3;
L6=B6+P+T3;
Length = [L1, L2, L3, L4, L5, L6];
Length = Length';

%% I don't think this is necessary, commented out for now
% % compute magnitude of vectors to solve for length
% length1=sqrt(L1(1)^2+L1(2)^2+L1(3)^2);
% length2=sqrt(L2(1)^2+L2(2)^2+L2(3)^2);
% length3=sqrt(L3(1)^2+L3(2)^2+L3(3)^2);
% length4=sqrt(L4(1)^2+L4(2)^2+L4(3)^2);
% length5=sqrt(L5(1)^2+L5(2)^2+L5(3)^2);
% length6=sqrt(L6(1)^2+L6(2)^2+L6(3)^2);
% length = [length1; length2; length3; length4; length5; length6];


end

