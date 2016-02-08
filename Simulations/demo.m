figure(1)
for i=1:101
    
clf
view([1 1 1])
axis([-1 1 -1 1 0 1])
hold on
[length1,l1,length2,l2,length3,l3,length4,l4,length5,l5,length6,l6]=traj(xdesired(i),ydesired(i),1+zdesired(i),anglex(i)+axtilt(i),angley(i)+aytilt(i),anglez(i));
quiver3(0.402*cos(10/180*pi),-0.402*sin(10/180*pi), 0,l1(1),l1(2),l1(3))

quiver3(0.402*cos(10/180*pi),0.402*sin(10/180*pi), 0,l2(1),l2(2),l2(3))

quiver3(0.402*cos(110/180*pi),0.402*sin(110/180*pi), 0,l3(1),l3(2),l3(3))

quiver3(0.402*cos(130/180*pi),0.402*sin(130/180*pi), 0,l4(1),l4(2),l4(3))

quiver3(0.402*cos(230/180*pi),0.402*sin(230/180*pi), 0,l5(1),l5(2),l5(3))

quiver3(0.402*cos(250/180*pi),0.402*sin(250/180*pi), 0,l6(1),l6(2),l6(3))



pause(0.1)
end