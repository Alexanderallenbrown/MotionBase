function [length1,L1,length2,L2,length3,L3 ,length4,L4 ,length5,L5 ,length6,L6] = traj(x2,y2,z2,ax,ay,az )

B1=[-0.402*cos(10/180*pi);0.402*sin(10/180*pi); 0];
P=[x2; y2; z2];
T1=[0.265*cos(30/180*pi); -0.265*sin(30/180*pi) ;0];

B2=[-0.402*cos(10/180*pi);-0.402*sin(10/180*pi); 0];
T2=[0.265*cos(30/180*pi); 0.265*sin(30/180*pi) ;0];

B3=[-0.402*cos(110/180*pi); -0.402*sin(110/180*pi); 0];
T3=[0; 0.265 ;0];

B4=[-0.402*cos(130/180*pi); -0.402*sin(130/180*pi); 0];
T4=[-0.265*cos(30/180*pi); 0.265*sin(30/180*pi) ;0];

B5=[0.402*cos(50/180*pi); 0.402*sin(50/180*pi); 0];
T5=[-0.265*cos(30/180*pi); -0.265*sin(30/180*pi) ;0];

B6=[0.402*cos(70/180*pi); 0.402*sin(70/180*pi); 0];
T6=[0;-0.265 ;0];

ax=ax/180*pi;
ay=ay/180*pi;
az=az/180*pi;

Rx=[1 0 0; 0 cos(ax) -sin(ax); 0 sin(ax) cos(ax)];
Ry=[cos(ay) 0 sin(ay); 0 1 0; -sin(ay) 0 cos(ay)];
Rz=[cos(az) -sin(az) 0; sin(az) cos(az) 0; 0 0 1];

T1=Rx*T1;
T1=Ry*T1;
T1=Rz*T1;

L1=B1+P+T1;

T2=Rx*T2;
T2=Ry*T2;
T2=Rz*T2;

L2=B2+P+T2;

T3=Rx*T3;
T3=Ry*T3;
T3=Rz*T3;

L3=B3+P+T3;

T4=Rx*T4;
T4=Ry*T4;
T4=Rz*T4;

L4=B4+P+T4;

T5=Rx*T5;
T5=Ry*T5;
T5=Rz*T5;

L5=B5+P+T5;

T6=Rx*T6;
T6=Ry*T6;
T6=Rz*T6;

L6=B6+P+T6;


length1=sqrt(L1(1)^2+L1(2)^2+L1(3)^2);
length2=sqrt(L2(1)^2+L2(2)^2+L2(3)^2);
length3=sqrt(L3(1)^2+L3(2)^2+L3(3)^2);
length4=sqrt(L4(1)^2+L4(2)^2+L4(3)^2);
length5=sqrt(L5(1)^2+L5(2)^2+L5(3)^2);
length6=sqrt(L6(1)^2+L6(2)^2+L6(3)^2);

end

