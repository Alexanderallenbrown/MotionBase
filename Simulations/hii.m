rawdata=xlsread('rawdata.xlsx');
%time,timestamp,recordtime,lat,long,alt,speed,course,verticalAccuracy,horizontalAccuracy,locTimeStamp,accelerationX,accelerationY,accelerationZ,HeadingX,HeadingY,HeadingZ,TrueHeading,MagneticHeading,HeadingAccuracy,RotationX,RotationY,RotationZ,motionYaw,motionRoll,motionPitch,motionRotationRateX,motionRotationRateY,motionRotationRateZ,motionUserAccelerationX,motionUserAccelerationY,motionUserAccelerationZ,en0,pdp_ip0,DeviceOrientation,Event
time=rawdata(:,2);
anglex=rawdata(:,19);
angley=rawdata(:,20);
anglez=rawdata(:,21);

ax=rawdata(:,11);
ay=rawdata(:,12);
az=rawdata(:,13);

signalax=[time,ax];
signalay=[time,ay];
signalaz=[time,az];

L1=[];
L2=[];
L3=[];
L4=[];
L5=[];
L6=[];

a11=[];
a12=[];
a21=[];
a22=[];
a31=[];
a32=[];
a41=[];
a42=[];
a51=[];
a52=[];
a61=[];
a62=[];

sim('demostration.slx')

for i=1:length(xdesired)
 
   [length1,l1,length2,l2,length3,l3,length4,l4,length5,l5,length6,l6]=traj(xdesired(i),ydesired(i),1+zdesired(i),anglex(i)+axtilt(i),angley(i)+aytilt(i),anglez(i)); 
   L1=[L1,length1];
   L2=[L2,length2];
   L3=[L3,length3];
   L4=[L4,length4];
   L5=[L5,length5];
   L6=[L6,length6];
   
%    [angle11,angle12]=legangle(l1,length1,1,1);
%    a11=[a11,angle11];
%    a12=[a12,angle12];
   
end

figure(1)
plot(time(1:101),L1)



