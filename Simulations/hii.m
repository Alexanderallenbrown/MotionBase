rawdata=xlsread('rawdata.csv');
time=rawdata(:,2);
ax=rawdata(:,19);
ay=rawdata(:,20);
az=rawdata(:,21);

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

for i=1:length(ax)
   [length1,l1,length2,l2,length3,l3,length4,l4,length5,l5,length6,l6]=traj(0,0,1,ax(i),ay(i),az(i)); 
   L1=[L1,length1];
   L2=[L2,length2];
   L3=[L3,length3];
   L4=[L4,length4];
   L5=[L5,length5];
   L6=[L6,length6];
   
   [angle11,angle12]=legangle(l1,length1,1,1);
   a11=[a11,angle11];
   a12=[a12,angle12];
   
end

figure(1)
plot(time,L1)

figure(2)
plot(time,az')
