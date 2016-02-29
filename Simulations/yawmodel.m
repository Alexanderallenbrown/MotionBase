clear all
close all
clc
% Establishing vehicle state space model for determination of yaw rate 
%parameters
Caf=-8.5*10^4;% %N/rad
Car=-10*10^4; % %N/rad
%U=18; %m/s
I=3000; %kg*m^2
m=2000; %kg
a=1; %m
b=1; %m
U=5;
figure()
hold on

plotStyle = {'b','k','r','g','b-.','k-.','r-.','g-.'}; % add as many as you need

for k = 1:8
%matrix A
U = 6*(k);
A=[(Caf+Car)/(m*U) (a*Caf-b*Car)/(m*U)-U;
    (a*Caf-b*Car)/(I*U) (a^2*Caf+b^2*Car)/(I*U)
];

%matrix B
B=[-Caf/m;
   -a*Caf/I 
];

%matrix C and D

C=[0 1];

D=[0];

C2 = [(Caf+Car)/(m*U) (a*Caf-b*Car)/(m*U)];
D2 = [-Caf/m];

%high pass filter
s=tf('s');
hp=s^2/(s^2+7*s+50);

[num_r,den_r]=ss2tf(A,B,C,D);
[num_ay,den_ay] = ss2tf(A,B,C2,D2);
delta_to_r(k) = tf(num_r,den_r);
delta_to_ay(k) = tf(num_ay,den_ay);
% subplot(1,2,1)
%hold on
% bode(delta_to_r(k)*hp,plotStyle{k})
% subplot(1,2,2)
% %hold on
% bode(delta_to_ay(k)*hp,plotStyle{k})
% legendInfo{k} = ['U = ' num2str(U)];




end
legend(legendInfo)
