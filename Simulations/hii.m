rawdata=xlsread('rawdata.xlsx');
%time,timestamp,recordtime,lat,long,alt,speed,course,verticalAccuracy,horizontalAccuracy,locTimeStamp,accelerationX,accelerationY,accelerationZ,HeadingX,HeadingY,HeadingZ,TrueHeading,MagneticHeading,HeadingAccuracy,RotationX,RotationY,RotationZ,motionYaw,motionRoll,motionPitch,motionRotationRateX,motionRotationRateY,motionRotationRateZ,motionUserAccelerationX,motionUserAccelerationY,motionUserAccelerationZ,en0,pdp_ip0,DeviceOrientation,Event
time=rawdata(:,2);
anglex=rawdata(:,19);
angley=rawdata(:,20);
anglez=rawdata(:,21);
RestHeight = 0.5;
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
op = 0.16;
pq = 1.2;
for i=1:length(xdesired)
 
   [length1,l1,length2,l2,length3,l3,length4,l4,length5,l5,length6,l6]=traj(xdesired(i),ydesired(i),RestHeight+zdesired(i),anglex(i)+axtilt(i),angley(i)+aytilt(i),anglez(i)); 
   L1=[L1,length1];
   L2=[L2,length2];
   L3=[L3,length3];
   L4=[L4,length4];
   L5=[L5,length5];
   L6=[L6,length6];
oq = l1;   
WrapFtnObj = @(ParmsPlaceHolder) mac(oq, op, pq, ParmsPlaceHolder);
InitAngle = 0;
OptAngle1(i) = fminsearch(WrapFtnObj, InitAngle);
   
   
%    [angle11,angle12]=legangle(l1,length1,0.16,1);
%    a11=[a11,angle11];
%    a12=[a12,angle12];
% 
%    [angle21,angle22]=legangle(l2,length2,0.16,1);
%    a21=[a21,angle21];
%    a22=[a22,angle22];
%    
%    [angle31,angle32]=legangle(l3,length3,0.16,1);
%    a31=[a31,angle31];
%    a32=[a32,angle32];
% 
%    [angle41,angle42]=legangle(l4,length4,0.16,1);
%    a41=[a41,angle41];
%    a42=[a42,angle42];
%    
%    [angle51,angle52]=legangle(l5,length5,0.16,1);
%    a51=[a51,angle51];
%    a52=[a52,angle52];
% 
%    [angle61,angle62]=legangle(l6,length6,0.16,1);
%    a61=[a61,angle61];
%    a62=[a62,angle62];
   
end

figure(1)
plot(time(1:101),a12)



