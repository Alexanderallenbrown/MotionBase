% Fixing Andy's script to find motor torques

rawdata=csvread('2015-01-24_11-49-26.csv');   % read roundabout data file
time1 = rawdata(:,2);                         % create a time vector

% actual angle, called "MotionRoll/Pitch/Yaw" in data --> checked by
% inspection of plot_roundabout_data.m
% raw values in radians
angle_x=rawdata(:,24);  
angle_y=rawdata(:,25);
angle_z=rawdata(:,26);

% linear acceleration, called "AccelerationX/Y/Z" in data
% raw values in g's --> convert to m/s^2
ax=rawdata(:,11).*9.81;
ay=rawdata(:,12).*9.81;
az=rawdata(:,13).*9.81;

% compose signals and send them to simulink
signal_x=[time1,ax];
signal_y=[time1,ay];
signal_z=[time1,az];

% run simulink --> output is axtilt, aytilt, xdesired, ydesired, zdesired
paramNameValStruct.StartTime = '0';
paramNameValStruct.StopTime = '45.77';
simOut = sim('demostration.slx', paramNameValStruct);
time = simOut.get('simtime');
ang_x = simOut.get('axtilt');
fix_ang_x = interp1(ang_x, time1);
angle_des = [angle_x + fix_ang_x, angle_y + simOut.get('aytilt'), angle_z];
motion_des = [simOut.find(xdesired), simOut.find(ydesired), 1+simOut.find(zdesired)];

