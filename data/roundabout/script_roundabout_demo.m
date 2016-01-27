clear all
close all
clc

addpath ../../MATLAB/GPS/

%time lat	long	alt	speed	course	verticalAccuracy	horizontalAccuracy	locTimeStamp	accelerationX	accelerationY	accelerationZ	HeadingX	HeadingY	HeadingZ	TrueHeading	MagneticHeading	HeadingAccuracy	RotationX	RotationY	RotationZ	motionYaw	motionRoll	motionPitch	motionRotationRateX	motionRotationRateY	motionRotationRateZ	motionUserAccelerationX	motionUserAccelerationY	motionUserAccelerationZ	en0	pdp_ip0	DeviceOrientation	State
d = load('chopped_2015-01-24_11-49-26.csv');%load data

t = d(:,1);
spd = d(:,5);
plot(t,spd,'k');
xlabel('Time (s)')
ylabel('Speed (m/s)')

figure
ax = -d(:,11);
plot(t,ax,'k')
xlabel('Time (s)')
ylabel('x-acceleration (g)')

lat = d(:,2);
lon = d(:,3);
alt = d(:,4);

for ind = 1:length(lat)
    enu = WGSLLA2ENU(lat(ind), lon(ind), alt(ind), lat(1), lon(1), alt(1));
    x(ind) = enu(1);
    y(ind) = enu(2);
    z(ind) = enu(3);
end

figure()
scatter(x,y,[],t,'o')
cb = colorbar('peer',gca);
set(get(cb,'ylabel'),'String','Time (s)')
axis equal
xlabel('East (m)')
ylabel('North (m)')

figure()
yaw = medfilt1(d(:,16),13);
course = d(:,6);
plot(t,yaw,t,course)

%now chop so that we get rid of repeat measurements.

indices = find(abs(diff(spd))>0);
spd = spd(indices);

x = x(indices);
y = y(indices);
t = t(indices);
course = course(indices);
%spd = spd(1:end-1);
v_east = [diff(x)'./diff(t)];
v_east = [v_east(1); v_east];

v_east_spd = spd.*sin(course*pi/180);

figure()
subplot(3,1,1)
plot(x,y)
axis equal
subplot(3,1,2)
plot(t,spd)
subplot(3,1,3)
plot(t,course)

figure()
plot(t,v_east,t,v_east_spd)

classdata_roundabout = [x' y' spd course];
save  classdata_roundabout.mat classdata_roundabout





