% testing values to get forces 1-6, using function forceplatform.m

acc = [0, 0, 0];
theta = [0, 0, 0];
m=10;
J=10;
Rpq1=[1,0,0];
Rpq2=[cos(60/180*pi),sin(60/180*pi),0];
Rpq3=[cos(120/180*pi),sin(120/180*pi),0];
Rpq4=[cos(180/180*pi),sin(180/180*pi),0];
Rpq5=[cos(240/180*pi),sin(240/180*pi),0];
Rpq6=[cos(300/180*pi),sin(300/180*pi),0];

[F] = forceplatform(m, J, Rpq1, Rpq2, Rpq3, Rpq4, Rpq5,Rpq6, acc, theta)



% e1=[0,0,1];
% e2=[0,0,1];
% e3=[0,0,1];
% e4=[0,0,1];
% e5=[0,0,1];
% e6=[0,0,1];

% [f1,f2,f3,f4,f5,f6]=forceplatform(ax,ay,az,alphax,alphay,alphaz,m,j,e1,e2,e3,e4,e5,e6,r1,r2,r3,r4,r5,r6)