clear

%% Define dimensions
r_base = 0.402;             % radius of platform, in m
r_platform = 0.265;         % radius of base, in m
shortleg = 0.16;            % length of motor arm, in m
longleg = 1;                % length of connecting rod, in m
z0_platform = 1;            % rest height of platform
m = 340/2.2;                % mass of platform   (from Inventor model)
J = [15.63, 35.35, 40.50];  % inertia, kg-m^2    (from Inventor model)

%% Read in raw data
rawdata=csvread('2015-01-24_11-49-26.csv');   % roundabout data file
time1 = rawdata(:,2);

% actual angle, called "MotionRoll/Pitch/Yaw" in data --> checked by
%   inspection of plot_roundabout_data.m
%   --> raw values in radians
angle_x=rawdata(:,24);
angle_y=rawdata(:,25);
angle_z=rawdata(:,26);
angle=[angle_x, angle_y, angle_z];

% linear acceleration, called "AccelerationX/Y/Z" in data
%   --> raw values in g's, want to convert to m/s^2
acc_x=rawdata(:,11).*9.81;
acc_y=rawdata(:,12).*9.81;
acc_z=rawdata(:,13).*9.81;
accel=[acc_x, acc_y, acc_z];

% compose signals for simulink
signal_x=[time1,accel(:,1)];
signal_y=[time1,accel(:,2)];
signal_z=[time1,accel(:,3)];

%% Run simulink motion cueing algorithm
%   --> output is axtilt, aytilt, xdesired, ydesired, zdesired
sim('demostration.slx');
motion_des = [xdesired, ydesired, zdesired];
angle_x = interp1(time1, angle(:,1), simtime);
angle_y = interp1(time1, angle(:,2), simtime);
angle_z = interp1(time1, angle(:,3), simtime);
angle_x= angle_x(~isnan(angle_x));
angle_y= angle_y(~isnan(angle_y));
angle_des = [angle_x(3:end)+axtilt, angle_y(3:end)+aytilt, angle_z(6:end)]; %% had to do stupid things to trim vectors, should fix this later %%

%% Run loop to determine platform position, motor arm angles, motor torques
% notation:
%       P = connection point between connecting rod and platform
%       Q = connection point between motor arm and connecting rod
%       O = connection point between motor arm and base
R_po = zeros(6,3);
R_pq = zeros(6,3);
error_pq = zeros(6,1);
F_pq = zeros(6,3);
Torque = zeros(6,3);
motor_angle = zeros(6,3);
initial = 0;        %   -->  what is this??
opt = zeros(6,1);
angle_qo = zeros(6,1);
r_qo(j) = [r_qo, opt];
[e(j), xx(j), yy(j), zz(j)] = angle(opt);
x = zeros(6,1);
y = zeros(6,1);
z = zeros(6,1);
error = zeros(6,1);

% angular velocity of short legs
thetaDx=[];
thetaDy=[];
thetaDz=[];

% angular acc of short legs
thetaDDx=[];
thetaDDy=[];
thetaDDz=[];

for i=1:length(xdesired)
    % solve for platform position and "leg" length, pause to see plot
    % (maybe)
    [R_po, base_points, platform_points, pos_motor] = platformposition(motion_des(i,:),angle_des(i,:), r_base, r_platform, z0_platform);
    pause(0.05)
    
    % find angles for motor arms
    for j = 1:6
        angle = @ (parm) findpq_leg(R_po(j,:), shortleg, longleg, pos_motor(j), parm);
        [opt(j)] = fminsearch(angle, initial);
        r_qo(j) = [r_qo(j), opt(j)];
        [e, xx, yy, zz] = angle(opt(j));
        x(j)=[x, xx];
        y(j)=[y, yy];
        z(j)=[z, zz];
        error(j)=[error, e];
    end
    
%     angle2=@ (parm) leg2(l2,shortleg,longleg,parm);
%     init2=[0];
%     [opt2]=fminsearch(angle2,init2);
%     %opt2=opt2/pi*180;
%     a2=[a2,opt2];
%     [e2,xx2,yy2,zz2]=angle2(opt2);
%     x2=[x2,xx2];
%     y2=[y2,yy2];
%     z2=[z2,zz2];
%     error2=[error2,e2];
    
    %vector from top base origin to top base links
    r_platform= [Tx(1),Ty(1),Tz(1)];
    r_base=[Tx(2),Ty(2),Tz(2)];
    r3=[Tx(3),Ty(3),Tz(3)];
    
    if i>1
        Dax=(angle_x(i)-angle_x(i-1))/0.05;
        Day=(angle_y(i)-angle_y(i-1))/0.05;
        Daz=0;
        
    else
        Dax=0;
        Day=0;
        Daz=0;
        
    end
    thetaDx=[thetaDx,Dax];
    thetaDy=[thetaDy,Day];
    thetaDz=[thetaDz,Daz];
    
    if i>2
        DDax=(thetaDx(i-1)-thetaDx(i-2))/0.05;
        DDay=(thetaDy(i-1)-thetaDy(i-2))/0.05;
        DDaz=0;
        
    else
        DDax=0;
        DDay=0;
        DDaz=0;
    end
    thetaDDx=[thetaDDx,DDax];
    thetaDDy=[thetaDDy,DDay];
    thetaDDz=[thetaDDz,DDaz];
    
    theta=[DDax,DDay,DDaz]/180*pi/4;
    
    %force on R_pq
    [f1,f2,f3,f4,f5,f6] = forceplatform(m, J, l1,l2,l3,l4,l5,l6,r_platform, r_base,r3,[acc_x(i),acc_y(i),acc_z(i)],theta);
    F1=[F1,f1];
    F2=[F2,f2];
    F3=[F3,f3];
    F4=[F4,f4];
    F5=[F5,f5];
    F6=[F6,f6];
    
    D1 = [-shortleg*cos(opt1)*sin(angle_qo(i)),shortleg*cos(opt1)*cos(angle_qo(i)),shortleg*sin(opt1)];
    
    Ll1 = [x1(i);y1(i);z1(i)];
    t1 = norm(cross(D1,Ll1)*f1/length);
    T1 = [T1,t1];
    
    D2 = [-shortleg*cos(opt2)*sin(a2(i)),shortleg*cos(opt2)*cos(a2(i)),shortleg*sin(opt2)];
    
    Ll2 = [x2(i);y2(i);z2(i)];
    t2 = norm(cross(D2,Ll2)*f2/length2);
    T2 = [T2,t2];
    
    D3 = [-shortleg*cos(opt3)*sin(a3(i)),shortleg*cos(opt3)*cos(a3(i)),shortleg*sin(opt3)];
    
    Ll3 = [x3(i);y3(i);z3(i)];
    t3 = norm(cross(D3,Ll3)*f3/length3);
    T3 = [T3,t3];
    
    D4 = [-shortleg*cos(opt4)*sin(a4(i)),shortleg*cos(opt4)*cos(a4(i)),shortleg*sin(opt4)];
    
    Ll4 = [x4(i);y4(i);z4(i)];
    t4 = norm(cross(D4,Ll4)*f4/length4);
    T4 = [T4,t4];
    
    D5 = [-shortleg*cos(opt5)*sin(a5(i)),shortleg*cos(opt5)*cos(a5(i)),shortleg*sin(opt5)];
    
    Ll5 = [x5(i);y5(i);z5(i)];
    t5 = norm(cross(D5,Ll5)*f5/length5);
    T5 = [T5,t5];
    
    D6 = [-shortleg*cos(opt6)*sin(a6(i)),shortleg*cos(opt6)*cos(a6(i)),shortleg*sin(opt6)];
    
    Ll6 = [x6(i);y6(i);z6(i)];
    t6 = norm(cross(D6,Ll6)*f6/length6);
    T6 = [T6,t6];
    
    
    
end

figure(1)
plot(F1)
title 'force on leg 1'

figure(2)
plot(T1)
title 'torque on leg 1'

for i = 1:100
    omega1(i) = (angle_qo(i+1)-angle_qo(i))/.05;
    omega2(i) = (a2(i+1)-a2(i))/.05;
    omega3(i) = (a3(i+1)-a3(i))/.05;
    omega4(i) = (a4(i+1)-a4(i))/.05;
    omega5(i) = (a5(i+1)-a5(i))/.05;
    omega6(i) = (a6(i+1)-a6(i))/.05;
end

figure(3)
plot(abs(omega1),T1(1:100),abs(omega2),T2(1:100),abs(omega3),T3(1:100),abs(omega4),T4(1:100),...
    abs(omega5),T5(1:100),abs(omega6),T6(1:100))

