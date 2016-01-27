
%% 


clear all
close all
clc

load('classdata_roundabout.mat')
%
x = classdata_roundabout(:,1);%m
y = classdata_roundabout(:,2);%m
speed = classdata_roundabout(:,3);%m/s
heading = classdata_roundabout(:,4);%deg
%


S(1) = 0;
for int = 1:44
    d(int)= ((x(int+1)-x(int))^2 + (y(int+1)-y(int))^2)^0.5
    S(int+1)=S(int)+d(int)
end

