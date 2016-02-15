rawdata=xlsread('rawdata.xlsx');
%time,timestamp,recordtime,lat,long,alt,speed,course,verticalAccuracy,horizontalAccuracy,locTimeStamp,accelerationX,accelerationY,accelerationZ,HeadingX,HeadingY,HeadingZ,TrueHeading,MagneticHeading,HeadingAccuracy,RotationX,RotationY,RotationZ,motionYaw,motionRoll,motionPitch,motionRotationRateX,motionRotationRateY,motionRotationRateZ,motionUserAccelerationX,motionUserAccelerationY,motionUserAccelerationZ,en0,pdp_ip0,DeviceOrientation,Event

time1 = rawdata(:,1);
anglex=rawdata(:,19);
angley=rawdata(:,20);
anglez=rawdata(:,21);

ax=rawdata(:,11);
ay=rawdata(:,12);
az=rawdata(:,13);

signalax=[time1,ax];
signalay=[time1,ay];
signalaz=[time1,az];

sim('demostration.slx');
time=simtime;
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


F1=[];
F2=[];
F3=[];
F4=[];
F5=[];
F6=[];

T1 = [];
T2 = [];
T3 = [];
T4 = [];
T5 = [];
T6 = [];
thetaDx=[];
thetaDy=[];
thetaDz=[];

thetaDDx=[];
thetaDDy=[];
thetaDDz=[];
for i=1:length(xdesired)
 
   [length1,l1,length2,l2,length3,l3,length4,l4,length5,l5,length6,l6,Bx,By,Bz,Tx,Ty,Tz]=traj(xdesired(i),ydesired(i),1+zdesired(i),anglex(i)+axtilt(i),angley(i)+aytilt(i),anglez(i)); 
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


r1= [Tx(1),Ty(1),Tz(1)];
r2=[Tx(2),Ty(2),Tz(2)];
r3=[Tx(3),Ty(3),Tz(3)];

if i>1
   Dax=(anglex(i)-anglex(i-1))/0.05;
   Day=(angley(i)-angley(i-1))/0.05;
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
m = 340/2.2;
J = [15.63, 35.35, 40.50]; %kg-m^2 Found from initial Inventor model


[f1,f2,f3,f4,f5,f6] = forceplatform(m, J, l1,l2,l3,l4,l5,l6,r1, r2,r3,[ax(i),ay(i),az(i)],theta);
F1=[F1,f1];
F2=[F2,f2];
F3=[F3,f3];
F4=[F4,f4];
F5=[F5,f5];
F6=[F6,f6];

D1 = [-shortleg*cos(opt1)*sin(a1(i)),shortleg*cos(opt1)*cos(a1(i)),shortleg*sin(opt1)];

Ll1 = [x1(i);y1(i);z1(i)];
t1 = norm(cross(D1,Ll1)*f1/length1);
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

figure(2)
plot(T1)

for i = 1:100
    omega1(i) = (a1(i+1)-a1(i))/.05;
    omega2(i) = (a2(i+1)-a2(i))/.05;
    omega3(i) = (a3(i+1)-a3(i))/.05;
    omega4(i) = (a4(i+1)-a4(i))/.05;
    omega5(i) = (a5(i+1)-a5(i))/.05;
    omega6(i) = (a6(i+1)-a6(i))/.05;
end

figure(3)
plot(abs(omega1),T1(1:100),abs(omega2),T2(1:100),abs(omega3),T3(1:100),abs(omega4),T4(1:100),...
    abs(omega5),T5(1:100),abs(omega6),T6(1:100))

