rawdata=xlsread('rawdata.xlsx');
%time
%time1 = rawdata(:,2);
time1=0:0.05:100;
delta=5*pi/180*sin(2*5*pi*time1);
input=[time1',delta'];
%actual tilt
% anglex=rawdata(:,20);
% angley=rawdata(:,21);
% anglez=rawdata(:,22);
% 
% %linear accelaration
% ax=rawdata(:,11);
% ay=rawdata(:,12);
% az=rawdata(:,13);
% 
% %compose signals and send them to simulink
% signalax=[time1,ax];
% signalay=[time1,ay];
% signalaz=[time1,az];
% % added roll pitch yaw, 2/16/16
% SignalRoll = [time1,anglex]; 
% SignalPitch = [time1,angley];
% SignalYaw = [time1,anglez];
% 
%run simulink
sim('demostration2.slx');
% time=simtime;


%initialize the length of the two legs
shortleg=0.16;
longleg=1;

%<<<<<<< HEAD
%L1 is the vector that records the length of leg1
%=======
% the length of the imaginary legs connecting point P to point O
%>>>>>>> 7d63f8bbbc886981d473b8914aaa42252d216686
L1=[];
L2=[];
L3=[];
L4=[];
L5=[];
L6=[];

%<<<<<<< HEAD
%a1 is the vector that record the angle of shortleg1
%=======
%these are the local motor angles for each of the motors.
%>>>>>>> 7d63f8bbbc886981d473b8914aaa42252d216686
a1=[];
a2=[];
a3=[];
a4=[];
a5=[];
a6=[];

%x y z 

%position of the points Q

x1=[];
y1=[];
z1=[];
%this is the distance error |PQ|
error1=[];

%the next few are the same for each of the 6 points
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

%these are the forces in the connecting rods 1-6
F1=[];
F2=[];
F3=[];
F4=[];
F5=[];
F6=[];

%these are the torques.....
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

for i=1:length(ydesired)
 
   z_default=1.06;
    
   [length1,l1,length2,l2,length3,l3,length4,l4,length5,l5,length6,l6,Bx,By,Bz,Tx,Ty,Tz]=traj(0,ydesired(i),z_default,axtilt(i)*180/pi,0,anglez(i)*180/pi); 
   L1=[L1,length1];
   L2=[L2,length2];
   L3=[L3,length3];
   L4=[L4,length4];
   L5=[L5,length5];
   L6=[L6,length6];
   
% angle1=@ (parm) leg11(l1,shortleg,longleg,parm);
% init1=[0];
% [opt1]=fminsearch(angle1,init1);
% %opt1=opt1/pi*180;
% a1=[a1,opt1];
% [e1,xx1,yy1,zz1]=angle1(opt1);
% x1=[x1,xx1];
% y1=[y1,yy1];
% z1=[z1,zz1];
% error1=[error1,e1];

[e1,xx1,yy1,zz1,opt1]=leg1(l1,shortleg,longleg);
a1=[a1,opt1];
error1=[error1,e1];
x1=[x1,xx1];
y1=[y1,yy1];
z1=[z1,zz1];

% angle2=@ (parm) leg2(l2,shortleg,longleg,parm);
% init2=[0];
% [opt2]=fminsearch(angle2,init2);
% %opt2=opt2/pi*180;

[e2,xx2,yy2,zz2,opt2]=leg2(l2,shortleg,longleg);
x2=[x2,xx2];
y2=[y2,yy2];
z2=[z2,zz2];
error2=[error2,e2];
a2=[a2,opt2];

[e3,xx3,yy3,zz3,opt3]=leg3(l3,shortleg,longleg);
x3=[x3,xx3];
y3=[y3,yy3];
z3=[z3,zz3];
error3=[error3,e3];
a3=[a3,opt3];

[e4,xx4,yy4,zz4,opt4]=leg4(l4,shortleg,longleg);
x4=[x4,xx4];
y4=[y4,yy4];
z4=[z4,zz4];
error4=[error4,e4];
a4=[a4,opt4];

[e5,xx5,yy5,zz5,opt5]=leg5(l5,shortleg,longleg);
x5=[x5,xx5];
y5=[y5,yy5];
z5=[z5,zz5];
error5=[error5,e5];
a5=[a5,opt5];

[e6,xx6,yy6,zz6,opt6]=leg6(l6,shortleg,longleg);
x6=[x6,xx6];
y6=[y6,yy6];
z6=[z6,zz6];
error6=[error6,e6];
a6=[a6,opt6];


% point of triangle connections 
r1= [Tx(1),Ty(1),Tz(1)];
r2=[Tx(2),Ty(2),Tz(2)];
r3=[Tx(3),Ty(3),Tz(3)];

%derivatives omega and alpha 
if i>1
   Dax=(axtilt(i)-axtilt(i-1))/0.05;
   %Day=(ayfiltered(i)-ayfiltered(i-1))/0.05;
   %Daz=0;
   
else
   Dax=0;
   % Day=0;
    %Daz=0;
      
end
   thetaDx=[thetaDx,Dax];
   %thetaDy=[thetaDy,Day];
  % thetaDz=[thetaDz,Daz];

if i>2
  DDax=(thetaDx(i-1)-thetaDx(i-2))/0.05;
   %DDay=(thetaDy(i-1)-thetaDy(i-2))/0.05;
 %  DDaz=0;
   
else
   DDax=0;
    %DDay=0;
   % DDaz=0;
end
  thetaDDx=[thetaDDx,DDax];
   %thetaDDy=[thetaDDy,DDay];
  % thetaDDz=[thetaDDz,DDaz];

theta=[DDax,0,0]/180*pi/4;
m = 340/2.2;
J = [15.63, 35.35, 40.50]; %kg-m^2 Found from initial Inventor model


[f1,f2,f3,f4,f5,f6] = forceplatform(m, J, l1,l2,l3,l4,l5,l6,r1, r2,r3,[0,ay(i),0],theta);
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
idx=size(error1,2);

figure(1)
plot(time1(1:idx),error1,time1(1:idx),error2,time1(1:idx),error3,time1(1:idx),error4,time1(1:idx),error5,time1(1:idx),error6)
xlabel('time')
ylabel('error(m)')
legend('1','2','3','4','5','6')
title('error, yaw freq@x tilt natural freq')

figure(2)
plot(T1)

% for i = 1:100
%     omega1(i) = (a1(i+1)-a1(i))/.05;
%     omega2(i) = (a2(i+1)-a2(i))/.05;
%     omega3(i) = (a3(i+1)-a3(i))/.05;
%     omega4(i) = (a4(i+1)-a4(i))/.05;
%     omega5(i) = (a5(i+1)-a5(i))/.05;
%     omega6(i) = (a6(i+1)-a6(i))/.05;
% end
% 
% figure(3)
% plot(abs(omega1(1:100)),T1(1:100),abs(omega2(1:100)),T2(1:100),abs(omega3(1:100)),T3(1:100),abs(omega4(1:100)),T4(1:100),...
%     abs(omega5(1:100)),T5(1:100),abs(omega6(1:100)),T6(1:100))

figure(4)

plot(anglez,a1,anglez,a2,anglez,a3,anglez,a4,anglez,a5,anglez,a6)
legend('Motor 1','Motor 2','Motor 3','Motor 4','Motor 5','Motor 6')
title('Platform yaw angle vs Motor Angles')
ylabel('Motor Angles (Rad)')
xlabel('Platform yaw Angle (degrees)')