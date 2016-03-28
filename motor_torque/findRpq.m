function [error, RpqX, RpqY, RpqZ] = findRpq(Rpo, motor_arm, conrod, pos_motor, a)
% finding vector pq based on a given angle
RpqX=Rpo(1)+motor_arm*cos(a)*sin(pos_motor);
RpqY=Rpo(2)-motor_arm*cos(a)*cos(pos_motor);
RpqZ=Rpo(3)-motor_arm*sin(a);

error = conrod - sqrt(RpqX^2+RpqY^2+RpqZ^2);

end