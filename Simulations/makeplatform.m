function [] = makeplatform(R_base, R_top
%       Inputs:     Base is a matrix, points 1-6 w/ coord x,y,z -> hexagon
%                   modeled by circle of radius R_base, points every 60 deg
%                           |1x 2x 3x 4x 5x 6x|
%                           |1y 2y 3y 4y 5y 6y|
%                           |1z 2z 3z 4z 5z 6z|
%                   Top is a matrix, points 7-9 w/ coord x,y,z -> triangle
%                   modeled by circle of radius R_top, points every 120 deg
%                           |7x 8x 9x|
%                           |7y 8y 9y|
%                           |7z 8z 9z|
%           
%

hex_angles = [-pi/6:pi/3:9*pi/6];
tri_angles = [0,2*pi/3,4*pi/3];

Base = [R_base.*cos(hex_angles)
    R_base.*sin(hex_angles)
    zeros(size(hex_angles))];
   
Top = [R_top.*cos(tri_angles)
    R_top.*sin(tri_angles)
    zeros(size(tri_angles))]; 
    




end