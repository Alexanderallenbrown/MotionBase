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
sim('demostration.slx');

shortleg=0.16;
longleg=1;

L1=[];
L2=[];
L3=[];
L4=[];
L5=[];
L6=[];

a1=[];
a2=[];
a3=[];
a4=[];
a5=[];
a6=[];

x1=[];
y1=[];
z1=[];
error1=[];

x2=[];
y2=[];
z2=[];
error2=[];

x3=[];
y3=[];
z3=[];
error3=[];

x4=[];
y4=[];
z4=[];
error4=[];

x5=[];
y5=[];
z5=[];
error5=[];

x6=[];
y6=[];
z6=[];
error6=[];

for i=1:length(xdesired)
 
   [length1,l1,length2,l2,length3,l3,length4,l4,length5,l5,length6,l6]=traj(xdesired(i),ydesired(i),1+zdesired(i),anglex(i)+axtilt(i),angley(i)+aytilt(i),anglez(i)); 
   L1=[L1,length1];
   L2=[L2,length2];
   L3=[L3,length3];
   L4=[L4,length4];
   L5=[L5,length5];
   L6=[L6,length6];
   
angle1=@ (parm) leg1(l1,shortleg,longleg,parm);
init1=[0];
[opt1]=fminsearch(angle1,init1);
%opt1=opt1/pi*180;
a1=[a1,opt1];
[e1,xx1,yy1,zz1]=angle1(opt1);
x1=[x1,xx1];
y1=[y1,yy1];
z1=[z1,zz1];
error1=[error1,e1];

angle2=@ (parm) leg2(l2,shortleg,longleg,parm);
init2=[0];
[opt2]=fminsearch(angle2,init2);
%opt2=opt2/pi*180;
a2=[a2,opt2];
[e2,xx2,yy2,zz2]=angle2(opt2);
x2=[x2,xx2];
y2=[y2,yy2];
z2=[z2,zz2];
error2=[error2,e2];


angle3=@ (parm) leg3(l3,shortleg,longleg,parm);
init3=[0];
[opt3]=fminsearch(angle3,init3);
%opt3=opt3/pi*180;
a3=[a3,opt3];
[e3,xx3,yy3,zz3]=angle3(opt3);
x3=[x3,xx3];
y3=[y3,yy3];
z3=[z3,zz3];
error3=[error3,e3];

angle4=@ (parm) leg4(l4,shortleg,longleg,parm);
init4=[0];
[opt4]=fminsearch(angle4,init4);
%opt4=opt4/pi*180;
a4=[a4,opt4];
[e4,xx4,yy4,zz4]=angle4(opt4);
x4=[x4,xx4];
y4=[y4,yy4];
z4=[z4,zz4];
error4=[error4,e4];

angle5=@ (parm) leg5(l5,shortleg,longleg,parm);
init5=[0];
[opt5]=fminsearch(angle5,init5);
%opt5=opt5/pi*180;
a5=[a5,opt5];
[e5,xx5,yy5,zz5]=angle5(opt5);
x5=[x5,xx5];
y5=[y5,yy5];
z5=[z5,zz5];
error5=[error5,e5];

angle6=@ (parm) leg6(l6,shortleg,longleg,parm);
init6=[0];
[opt6]=fminsearch(angle6,init6);
%opt6=opt6/pi*180;
a6=[a6,opt6];
[e6,xx6,yy6,zz6]=angle6(opt6);
x6=[x6,xx6];
y6=[y6,yy6];
z6=[z6,zz6];
error6=[error6,e6];

end

figure(1)
plot(error1)



