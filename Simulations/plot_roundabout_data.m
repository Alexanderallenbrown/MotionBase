rawdata=xlsread('2015-01-24_11-49-26.csv');   % read truck roundabout data file

time = rawdata(:,2);    % create a time vector

figure()
hold on
plot(time, rawdata(:,13))
plot(time, rawdata(:,16))
plot(time, rawdata(:,22))
plot(time, rawdata(:,25))
plot(time, rawdata(:,28))
legend('AccelZ','HeadingZ','RotationZ','MotionPitch','MotionRotationRateZ')
title 'Z axis'
hold off

figure()
hold on
plot(time, rawdata(:,12))
plot(time, rawdata(:,15))
plot(time, rawdata(:,21))
plot(time, rawdata(:,24))
plot(time, rawdata(:,27))
legend('AccelY','HeadingY','RotationY','MotionRoll','MotionRotationRateY')
title 'Y axis'
hold off

figure()
hold on
plot(time, rawdata(:,11))
plot(time, rawdata(:,14))
plot(time, rawdata(:,20))
plot(time, rawdata(:,23))
plot(time, rawdata(:,26))
legend('AccelX','HeadingX','RotationX','MotionYaw','MotionRotationRateX')
title 'X axis'
hold off
