close all
clear all
clc

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
angle_x=rawdata(:,26);%CHECK THESE COLUMN ORDERS!!!
angle_y=rawdata(:,25);
angle_z=rawdata(:,24);
angle=[angle_x, angle_y, angle_z];

% linear acceleration, called "AccelerationX/Y/Z" in data
%   --> raw values in g's, want to convert to m/s^2
acc_x=rawdata(:,13).*9.81;
acc_y=rawdata(:,12).*9.81;%THESE DIRECTIONS ARE OUT OF ORDER. WEIRD
acc_z=rawdata(:,14).*9.81;%NOW THESE ARE IN M/S/S SO MAKE SURE SIM IS TOO!
accel=[acc_x, acc_y, acc_z+9.81];%added g to z to offset gravity. This is meh....

% compose signals for simulink
signal_x=[time1,accel(:,1)];
signal_y=[time1,accel(:,2)];
signal_z=[time1,accel(:,3)];

figure()
subplot(3,1,1)
plot(signal_x(:,1),signal_x(:,2))
ylabel('ax')
subplot(3,1,2)
plot(signal_y(:,1),signal_y(:,2))
ylabel('ay')
subplot(3,1,3)
plot(signal_z(:,1),signal_z(:,2))
xlabel('Time (s)')
ylabel('az')
%% Run simulink motion cueing algorithm
%   --> output is axtilt, aytilt, xdesired, ydesired, zdesired
sim('demostration1.slx');
motion_des = [xdesired, ydesired, zdesired];
angle_x = interp1(time1, angle(:,1), simtime);
angle_y = interp1(time1, angle(:,2), simtime);
angle_z = interp1(time1, angle(:,3), simtime);
%angle_x= angle_x(~isnan(angle_x));
%angle_y= angle_y(~isnan(angle_y));

%angle_des = [angle_x(3:end)+axtilt, angle_y(3:end)+aytilt, angle_z(6:end)]; %% had to do stupid things to trim vectors, should fix this later %%
angle_des = [angle_x+axtilt, angle_y+aytilt, zeros(size(angle_z))]; %% had to do stupid things to trim vectors, should fix this later %%
%MEGAN-- WE NEED TO FIX THE ANGLE Z. We can't ask for angle z directly...
%needs to be high pass filtered!!! Grab this from Dallis's branch and paste
%into your simulink??

%% Calculate linear velocity, acceleration and angular velocity, acceleration    
vel_desX(:,1) = [0; diff(motion_des(:,1))./diff(simtime)];      % split into XYZ to make sure diff works in the right direction
vel_desY(:,2) = [0; diff(motion_des(:,2))./diff(simtime)];
vel_desZ(:,3) = [0; diff(motion_des(:,3))./diff(simtime)];

acc_desX(:,1) = [0; diff(vel_desX)./diff(simtime)];
acc_desY(:,2) = [0; diff(vel_desY(:,2))./diff(simtime)];
acc_desZ(:,3) = [0; diff(vel_desZ(:,3))./diff(simtime)];

omega_desX(:,1) = [0; diff(angle_des(:,1))./diff(simtime)];
omega_desY(:,2) = [0; diff(angle_des(:,2))./diff(simtime)];
omega_desZ(:,3) = [0; diff(angle_des(:,3))./diff(simtime)];

alpha_desX(:,1) = [0; diff(omega_desX)./diff(simtime)];
alpha_desY(:,2) = [0; diff(omega_desY(:,2))./diff(simtime)];
alpha_desZ(:,3) = [0; diff(omega_desZ(:,3))./diff(simtime)];
    
vel_des = [vel_desX, vel_desY(:,2), vel_desZ(:,3)];   % compose into nice matrices
acc_des = [acc_desX, acc_desY(:,2), acc_desZ(:,3)];
omega_des = [omega_desX, omega_desY(:,2), omega_desZ(:,3)];
alpha_des = [alpha_desX, alpha_desY(:,2), alpha_desZ(:,3)];

figure()
subplot(2,2,1)
hold on
plot(simtime,vel_desX)
plot(simtime,vel_desY)
plot(simtime,vel_desY)
xlabel 'time'
ylabel 'desired velocity'
legend('X', 'Y', 'Z')
hold off
subplot(2,2,2)
hold on
plot(simtime,acc_desX)
plot(simtime,acc_desY)
plot(simtime,acc_desZ)
xlabel 'time'
ylabel 'desired acceleration'
legend('X', 'Y', 'Z')
hold off
subplot(2,2,3)
hold on
plot(simtime,omega_desX)
plot(simtime,omega_desY)
plot(simtime,omega_desZ)
xlabel 'time'
ylabel 'desired angular velocity'
legend('X', 'Y', 'Z')
hold off
subplot(2,2,4)
hold on
plot(simtime,alpha_desX)
plot(simtime,alpha_desY)
plot(simtime,alpha_desZ)
xlabel 'time' 
ylabel 'desired angular acceleration'
legend('X', 'Y', 'Z')
hold off

pause

% figure()
% hold on
% plot(time1,accel)
% plot(simtime,acc_des)
% hold off
% xlabel 'time'
% ylabel 'accel'
% legend()

%% Run loop to determine platform position, motor arm angles, motor torques
% notation:
%       P = connection point between connecting rod and platform
%       Q = connection point between motor arm and connecting rod
%       O = connection point between motor arm and base
%       G = 0,0,0 (ground)
R_po = zeros(6,3);
R_pq = zeros(6,3);
R_qo = zeros(6,3);
F_pq = zeros(6,3);
Torque = zeros(6,3);
motor_angle = zeros(6,3);
initial = 0;        %   -->  what is this??
opt = zeros(6,1);
x = zeros(6,1);
y = zeros(6,1);
z = zeros(6,1);
error = zeros(6,1);
T = zeros(6,1);
T_qo = zeros(6,3);
Rpq_x = zeros(6,1);
Rpq_y = zeros(6,1);
Rpq_z = zeros(6,1);
Rqo_x = zeros(6,1);
Rqo_y = zeros(6,1);
Rqo_z = zeros(6,1);
T_qo_x = zeros(6,1);
T_qo_y = zeros(6,1);
T_qo_z = zeros(6,1);

%plot the desired angles
figure()
plot(simtime,angle_des(:,1),simtime,angle_des(:,2),simtime,angle_des(:,3))
xlabel('Time (s)')
ylabel('Desired angles')
legend('x','y','z')

figure()
plot(simtime,motion_des(:,1),simtime,motion_des(:,2),simtime,motion_des(:,3))
xlabel('Time (s)')
ylabel('Desired motion')
legend('x','y','z')

pause


%create a matrix to store torques for each motor
Motor_Torques = zeros(length(simtime),6);%done
Motor_angular_vels = zeros(length(simtime),6);%todo store this way
Motor_angular_accels = zeros(length(simtime),6);%todo store this way


for i=1:length(motion_des)    % motion index
    % solve for platform position and "leg" length, pause to see plot
    % (maybe)
    [R_po, motors, platform_points, motorangles, R_pc] = platformposition(motion_des(i,:),angle_des(i,:), r_base, r_platform, z0_platform);
    
    cla()
    % compose stuff for plotting, change this later
    hold on
    grid on
    platformX = [platform_points(1,1),platform_points(2,1),platform_points(3,1),platform_points(1,1)];
    platformY = [platform_points(1,2),platform_points(2,2),platform_points(3,2),platform_points(1,2)];
    platformZ = [platform_points(1,3),platform_points(2,3),platform_points(3,3),platform_points(1,3)];
    baseX = [motors(1,1),motors(2,1),motors(3,1),motors(4,1),motors(5,1),motors(6,1),motors(1,1)];
    baseY = [motors(1,2),motors(2,2),motors(3,2),motors(4,2),motors(5,2),motors(6,2),motors(1,2)];
    baseZ = [motors(1,3),motors(2,3),motors(3,3),motors(4,3),motors(5,3),motors(6,3),motors(1,3)];
    
    % find angles for motor arms using fminsearch
    for j = 1:6             % leg index
        %find this motor angle
        angle = @ (parm) findpq_leg(R_po(j,:), shortleg, longleg, motorangles(j), parm);
        [opt(i,j)] = fminsearch(angle, initial);
        [error, x, y, z] = angle(opt(i,j));
        R_pq = [x, y, z];
        R_qo = R_po(j,:) - R_pq;
        Rpq_x(j) = R_pq(1);     % had to disassemble R_pq so that it would write to j
        Rpq_y(j) = R_pq(2);
        Rpq_z(j) = R_pq(3);
        Rqo_x(j) = R_qo(1);
        Rqo_y(j) = R_qo(2);
        Rqo_z(j) = R_qo(3);
    end
    
    R_pq = [Rpq_x, Rpq_y, Rpq_z];       % reassemble
    R_qo = [Rqo_x, Rqo_y, Rqo_z];
    R_pg = platform_points;%calculate global location of points P. just call it the right thing... not used at the moment.
    
    % find force, torque on each leg
    for k = 1:6
        [F_pq] = forceplatform(m, J, R_pq(1,:), R_pq(2,:), R_pq(3,:), R_pq(4,:), R_pq(5,:), R_pq(6,:), R_pc(1,:), R_pc(2,:), R_pc(3,:), acc_des(i,:), alpha_des(i,:));
        
        for index_m = 1:6
            T_qo = cross(R_qo(index_m,:), -F_pq(index_m,:));
            T_qo_x(index_m) = T_qo(1);     % had to disassemble R_pq so that it would write to j
            T_qo_y(index_m) = T_qo(2);
            T_qo_z(index_m) = T_qo(3);
        end
        
        T_qo = [T_qo_x, T_qo_y, T_qo_z];    % reassemble
        T(k) = norm(T_qo);
        %store this in the matrix...
        Motor_Torques(i,k) = norm(T_qo);%eventually delete the line above. TODO dot product.
        
        %         e_motorX = cos(motorangles');
        %         e_motorY = sin(motorangles');
        %         e_motorZ = zeros(1,6);
        %         e_motor = [e_motorX, e_motorY, e_motorZ]; %%%this needs fixing
        %         T(k) = dot(e_motor(k,:), T_qo(k,:));
    end

end
hold off

%% calculate angular velocity
omega = zeros(size(Motor_Torques));

for n = 1:6
    opt_new = opt(:,n);               % split angle matrix into columns
    for i=1:length(opt_new)        % motion index
        if i>1
            omega(i,n)= (opt_new(i)-opt_new(i-1))/(simtime(i)-simtime(i-1));
        else
            omega(i,n) = 0;
        end
    end
end

%plot motor angles
figure()
plot(simtime,opt(:,1),simtime,opt(:,2),simtime,opt(:,3),simtime,opt(:,4),simtime,opt(:,5),simtime,opt(:,6))
hold on
plot([min(simtime) max(simtime)],[0,0],'r','LineWidth',4)
plot([min(simtime) max(simtime)],[pi/4,pi/4],'r','LineWidth',4)
legend('motor 1','motor 2','motor 3','motor 4','motor 5','motor 6','motor limits')
xlabel('Time (s)')
ylabel('motor arm angle requested (rad)')

% filter data
om = medfilt1(omega,13);
torque = medfilt1(Motor_Torques,13);

figure()
hold on
plot(abs(om),torque, '.')
xlim([0, 3])
ylim([0, 400])
xlabel 'Omega (rad/s)'
ylabel 'Torque (N-m)'
hold off


