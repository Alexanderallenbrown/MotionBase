function [ a1,a2] = legangle( L1,length1,length2,length3 )

a2=acos((length2^2+length3^2-length1^2)/(2*length2*length3));
a3=acos((length1^2+length2^2-length3^2)/(2*length2*length1));
a4=acos(L1(1)/length1);
a1=a4-a3;

a2=a2/pi*180;
a1=a1/pi*180;

end

