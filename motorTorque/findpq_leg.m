function [error, x, y, z] = findpq_leg(Rpo, motor_arm, conrod, pos_motor, angle)
% finding vector pq based on a given angle
x=Rpo(1)+motor_arm*cos(a)*sin(pos_motor);
y=Rpo(2)-motor_arm*cos(a)*cos(pos_motor);
z=Rpo(3)-motor_arm*sin(a);

error=abs(conrod-sqrt(x^2+y^2+z^2));

end