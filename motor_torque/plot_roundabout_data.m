clear
close all

rawdata=csvread('2015-01-24_11-49-26.csv');   % read truck roundabout data file

%time,timestamp,recordtime,lat,long,alt,speed,course,verticalAccuracy,horizontalAccuracy,locTimeStamp,accelerationX,accelerationY,accelerationZ,HeadingX,HeadingY,HeadingZ,TrueHeading,MagneticHeading,HeadingAccuracy,RotationX,RotationY,RotationZ,motionYaw,motionRoll,motionPitch,motionRotationRateX,motionRotationRateY,motionRotationRateZ,motionUserAccelerationX,motionUserAccelerationY,motionUserAccelerationZ,en0,pdp_ip0,DeviceOrientation,State
%  1    2           3       4   5   6     7     8           9


time = rawdata(:,2);    % create a time vector

figure()
hold on
plot(time, rawdata(:,14))
plot(time, rawdata(:,17)*pi/180)
plot(time, rawdata(:,23))
plot(time, rawdata(:,26))
plot(time, rawdata(:,29))
legend('AccelZ','HeadingZ','RotationZ','MotionYaw','MotionRotationRateZ')
title 'Z axis'
hold off

figure()
hold on
plot(time, rawdata(:,13))
plot(time, rawdata(:,16)*pi/180)
plot(time, rawdata(:,22))
plot(time, rawdata(:,25))
plot(time, rawdata(:,28))
ylim([-3 3])
legend('AccelY','HeadingY','RotationY','MotionPitch','MotionRotationRateY')
title 'Y axis'
hold off

figure()
hold on
plot(time, rawdata(:,12))
plot(time, rawdata(:,15)*pi/180)
plot(time, rawdata(:,21))
plot(time, rawdata(:,24))
plot(time, rawdata(:,27))
legend('AccelX','HeadingX','RotationX','MotionRoll','MotionRotationRateX')
title 'X axis'
hold off
