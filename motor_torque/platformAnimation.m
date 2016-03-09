function [] = platformAnimation()

    % just for plotting
    motorarm1X = [motors(1,1), R_qo(1,1)+motors(1,1)];
    motorarm2X = [motors(2,1), R_qo(2,1)+motors(2,1)];
    motorarm3X = [motors(3,1), R_qo(3,1)+motors(3,1)];
    motorarm4X = [motors(4,1), R_qo(4,1)+motors(4,1)];
    motorarm5X = [motors(5,1), R_qo(5,1)+motors(5,1)];
    motorarm6X = [motors(6,1), R_qo(6,1)+motors(6,1)];
    
    motorarm1Y = [motors(1,2), R_qo(1,2)+motors(1,2)];
    motorarm2Y = [motors(2,2), R_qo(2,2)+motors(2,2)];
    motorarm3Y = [motors(3,2), R_qo(3,2)+motors(3,2)];
    motorarm4Y = [motors(4,2), R_qo(4,2)+motors(4,2)];
    motorarm5Y = [motors(5,2), R_qo(5,2)+motors(5,2)];
    motorarm6Y = [motors(6,2), R_qo(6,2)+motors(6,2)];
    
    motorarm1Z = [motors(1,3), R_qo(1,3)+motors(1,3)];
    motorarm2Z = [motors(2,3), R_qo(2,3)+motors(2,3)];
    motorarm3Z = [motors(3,3), R_qo(3,3)+motors(3,3)];
    motorarm4Z = [motors(4,3), R_qo(4,3)+motors(4,3)];
    motorarm5Z = [motors(5,3), R_qo(5,3)+motors(5,3)];
    motorarm6Z = [motors(6,3), R_qo(6,3)+motors(6,3)];
    
    motorarm1X = [motors(1,1), R_qo(1,1)+motors(1,1)];
    motorarm2X = [motors(2,1), R_qo(2,1)+motors(2,1)];
    motorarm3X = [motors(3,1), R_qo(3,1)+motors(3,1)];
    motorarm4X = [motors(4,1), R_qo(4,1)+motors(4,1)];
    motorarm5X = [motors(5,1), R_qo(5,1)+motors(5,1)];
    motorarm6X = [motors(6,1), R_qo(6,1)+motors(6,1)];
    
    motorarm1Y = [motors(1,2), R_qo(1,2)+motors(1,2)];
    motorarm2Y = [motors(2,2), R_qo(2,2)+motors(2,2)];
    motorarm3Y = [motors(3,2), R_qo(3,2)+motors(3,2)];
    motorarm4Y = [motors(4,2), R_qo(4,2)+motors(4,2)];
    motorarm5Y = [motors(5,2), R_qo(5,2)+motors(5,2)];
    motorarm6Y = [motors(6,2), R_qo(6,2)+motors(6,2)];
    
    motorarm1Z = [motors(1,3), R_qo(1,3)+motors(1,3)];
    motorarm2Z = [motors(2,3), R_qo(2,3)+motors(2,3)];
    motorarm3Z = [motors(3,3), R_qo(3,3)+motors(3,3)];
    motorarm4Z = [motors(4,3), R_qo(4,3)+motors(4,3)];
    motorarm5Z = [motors(5,3), R_qo(5,3)+motors(5,3)];
    motorarm6Z = [motors(6,3), R_qo(6,3)+motors(6,3)];
    
    
    plot3(motorarm1X, motorarm1Y, motorarm1Z);
    plot3(motorarm2X, motorarm2Y, motorarm2Z);
    plot3(motorarm3X, motorarm3Y, motorarm3Z);
    plot3(motorarm4X, motorarm4Y, motorarm4Z);
    plot3(motorarm5X, motorarm5Y, motorarm5Z);
    plot3(motorarm6X, motorarm6Y, motorarm6Z);
    plot3(platformX, platformY, platformZ);
    plot3(baseX, baseY, baseZ)
    view(-205,45)
    pause(0.01)
    zlim([-0.5 1.5])
    