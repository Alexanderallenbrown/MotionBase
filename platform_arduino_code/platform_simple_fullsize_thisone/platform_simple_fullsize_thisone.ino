// ONLY USE ARDUINO 1.0.6 WITH THIS CODE

/* <Controlling code for Arduino Controlled Rotary Stewart Platform>
    Copyright (C) <2014>  <Tomas Korgo>
    
    Modified and simplified by Alexander Brown 2016

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.*/

#include <Servo.h>
#include <Wire.h>


//MIN and MAX PWM pulse sizes, they can be found in servo documentation
#define MAX 2200
#define MIN 800

//Positions of servos mounted in opposite direction
#define INV1 1
#define INV2 3
#define INV3 5

//constants for computation of positions of connection points
#define pi  3.14159
#define deg2rad 180/pi
#define deg30 pi/6

//these are the absolute limits of motion that we will allow.
float pos_limit = 3;
float ang_limit = 0.2;

unsigned long time;

//ALL DIMENSIONS IN THIS CODE ARE IN INCHES
//Array of servo objects
Servo servo[6];
//Zero positions of servos, in this positions their arms are perfectly horizontal, in us
static int zero[6]={1470,1470,1470,1470,1470,1470};
//In this array is stored requested position for platform - x,y,z,rot(x),rot(y),rot(z)
static float arr[6]={0,0.0,0, radians(0),radians(0),radians(0)};
//Actual degree of rotation of all servo arms, they start at 0 - horizontal, used to reduce
//complexity of calculating new degree of rotation
static float theta_a[6]={0.0,0.0,0.0, 0.0,0.0,0.0};
//Array of current servo positions in us
static int servo_pos[6];
//rotation of servo arms in respect to axis x
const float beta[] = {pi/2,-pi/2,-pi/6, 5*pi/6,-5*pi/6,pi/6},
//const float beta[] = {pi/6, pi/2, 5*pi/6, -5*pi/6, -pi/2, -pi/6},
//maximum servo positions, 0 is horizontal position
servo_min=radians(-80),servo_max=radians(80),
//servo_mult - multiplier used for conversion radians->servo pulse in us
//L1-effective length of servo arm, L2 - length of base and platform connecting arm
//z_home - height of platform above base, 0 is height of servo arms
//servo_mult=400/(pi/4),L1 = 0.79,L2 = 4.66, z_home = 4.05;
servo_mult=400/(pi/4),L1 = 6.25,L2 = 24.00, z_home = 20.00;
//RD distance from center of platform to attachment points (arm attachment point)
//PD distance from center of base to center of servo rotation points (servo axis)
//theta_p-angle between two servo axis points, theta_r - between platform attachment points
//theta_angle-helper variable
//p[][]=x y values for servo rotation points
//re[]{}=x y z values of platform attachment points positions
//equations used for p and re will affect postion of X axis, they can be changed to achieve
//specific X axis position
//const float RD = 2.42,PD =2.99,theta_p = radians(37.5),
const float RD = 16.00,PD = 27.00,theta_p = radians(37.5),
theta_angle=(pi/3-theta_p)/2, theta_r = radians(8),
//      p[2][6]={
//        {
//            PD*sin(theta_angle),
//          PD*cos(deg30+theta_angle),
//            PD*cos(deg30+theta_angle),
//          PD*sin(theta_angle),
//          -PD*cos(deg30-theta_angle),
//           -PD*cos(deg30-theta_angle) 
//         }, // x values
//         {
//           PD*cos(theta_angle),
//           PD*sin(deg30+theta_angle),
//           -PD*sin(deg30+theta_angle),
//           -PD*cos(theta_angle),
//           -PD*sin(deg30-theta_angle),
//           PD*sin(deg30-theta_angle)
//         } // y values
//      },
//      re[3][6] = {
//          {
//              -RD*sin(deg30-theta_r/2),
//              RD*cos(theta_r/2),
//              RD*cos(theta_r/2),
//              -RD*sin(deg30-theta_r/2),
//              -RD*sin(deg30+theta_r/2),
//              -RD*sin(deg30+theta_r/2)
//          },{
//              RD*cos(deg30-theta_r/2),
//              RD*sin(theta_r/2),
//              -RD*sin(theta_r/2),
//              -RD*cos(deg30-theta_r/2),
//              -RD*cos(deg30+theta_r/2),
//              RD*cos(deg30+theta_r/2)      
//          },{
//              0,0,0,0,0,0
//          }
//};

      p[2][6]={
          {
            -PD*cos(deg30-theta_angle),-PD*cos(deg30-theta_angle),
            PD*sin(theta_angle),PD*cos(deg30+theta_angle),
            PD*cos(deg30+theta_angle),PD*sin(theta_angle)
         },
         {
            -PD*sin(deg30-theta_angle),PD*sin(deg30-theta_angle),
            PD*cos(theta_angle),PD*sin(deg30+theta_angle),
            -PD*sin(deg30+theta_angle),-PD*cos(theta_angle)
         }
      },
      re[3][6] = {
          {
              -RD*sin(deg30+theta_r/2),-RD*sin(deg30+theta_r/2),
              -RD*sin(deg30-theta_r/2),RD*cos(theta_r/2),
              RD*cos(theta_r/2),-RD*sin(deg30-theta_r/2),
          },{
              -RD*cos(deg30+theta_r/2),RD*cos(deg30+theta_r/2),
              RD*cos(deg30-theta_r/2),RD*sin(theta_r/2),
              -RD*sin(theta_r/2),-RD*cos(deg30-theta_r/2),
          },{
              0,0,0,0,0,0
          }
};

//arrays used for servo rotation calculation
//H[]-center position of platform can be moved with respect to base, this is
//translation vector representing this move
static float M[3][3], rxp[3][6], T[3], H[3] = {0,0,z_home};

void setup(){
  
  Serial.setTimeout(5); // testing for delay source
  
//attachment of servos to PWM digital pins of arduino
   servo[0].attach(3, MIN, MAX);
   servo[1].attach(5, MIN, MAX);
   servo[2].attach(6, MIN, MAX);
   servo[3].attach(9, MIN, MAX);
   servo[4].attach(10, MIN, MAX);
   servo[5].attach(11, MIN, MAX);
//begin of serial communication
   Serial.begin(115200);
   Serial.println("welcome to the motion platform");
//putting into base position
   setPos(arr);
}


//main control loop, obtain requested action from serial connection, then execute it
void loop()
{
  //read a list of 6 floats from the serial port (python/MATLAB) representing the desired positions [x,y,z,r,p,y] with x,y,z in mm and r,p,y in rad.
  //looks for a newline character, and the rest of the numbers are separated by commas.
  
//let's kill any buffered serial data
  while(Serial.available()>256){
    byte junk = Serial.read();
 }
  
  while(Serial.available()>0){
    
    if(Serial.read()=='!'){
      
      float px = Serial.parseFloat();
      float py = Serial.parseFloat();
      float pz = Serial.parseFloat();
      float pr = Serial.parseFloat();
      float pp = Serial.parseFloat();
      float pa = Serial.parseFloat();
      
    
      if (abs(px)>pos_limit){
        px = pos_limit*sgn(px)*100;
      }
      if (abs(py)>pos_limit){
        py = pos_limit*sgn(py)*100;
      }
      if (abs(pz)>pos_limit){
        pz = pos_limit*sgn(pz)*100;
      }
      if (abs(pr)>ang_limit){
        pr = ang_limit*sgn(pr);
      }
      if (abs(pp)>ang_limit){
        pp = ang_limit*sgn(pp);
      }
      if (abs(pa)>ang_limit){
        pa = ang_limit*sgn(pa);
      }
    
    if(Serial.read()=='\n'){
     //arr[6] = {px,py,pz,pr,pp,pa};//set the values for the platform 
     arr[0] = px;
     arr[1] = py;
     arr[2] = pz;
     arr[3] = pr;
     arr[4] = pp;
     arr[5] = pa;
     
//     //print back to the monitor
//     Serial.print(millis());
//     Serial.print(",");
//     Serial.print(px);
//     Serial.print(",");
//     Serial.print(py);
//     Serial.print(",");
//     Serial.print(pz);
//     Serial.print(",");
//     Serial.print(pr);
//     Serial.print(",");
//     Serial.print(pp);
//     Serial.print(",");
//     Serial.print(pa);
//     Serial.println();
     
     //print back to the monitor
     Serial.print(millis());
     Serial.print(",");
     Serial.print(px);
     Serial.print(",");
     Serial.print(py);
     Serial.print(",");
     Serial.print(pz);
     Serial.print(",");
     Serial.print(pr);
     Serial.print(",");
     Serial.print(pp);
     Serial.print(",");
     Serial.print(pa);
     Serial.println();     
     
     //write to the base
     //Serial.write("hello,");
     Serial.flush();
     setPos(arr); 
  
    }
    }
  }
delay(10);

}



//function calculating needed servo rotation value
float getAlpha(int *i){
   static int n;
   static float th=0;
   static float q[3], dl[3], dl2;
   double min=servo_min;
   double max=servo_max;
   n=0;
   th=theta_a[*i];
   while(n<20){
    //calculation of position of base attachment point (point on servo arm where is leg connected)
      q[0] = L1*cos(th)*cos(beta[*i]) + p[0][*i];
      q[1] = L1*cos(th)*sin(beta[*i]) + p[1][*i];
      q[2] = L1*sin(th);
    //calculation of distance between according platform attachment point and base attachment point
      dl[0] = rxp[0][*i] - q[0];
      dl[1] = rxp[1][*i] - q[1];
      dl[2] = rxp[2][*i] - q[2];
      dl2 = sqrt(dl[0]*dl[0] + dl[1]*dl[1] + dl[2]*dl[2]);
    //if this distance is the same as leg length, value of theta_a is corrent, we return it
      if(abs(L2-dl2)<0.01){
         return th;
      }
    //if not, we split the searched space in half, then try next value
      if(dl2<L2){
         max=th;
      }else{
         min=th;
      }
      n+=1;
      if(max==servo_min || min==servo_max){
         return th;
      }
      th = min+(max-min)/2;
   }
   return th;
}

//function calculating rotation matrix
void getmatrix(float pe[])
{
   float psi=pe[5];
   float theta=pe[4];
   float phi=pe[3];
   M[0][0] = cos(psi)*cos(theta);
   M[1][0] = -sin(psi)*cos(phi)+cos(psi)*sin(theta)*sin(phi);
   M[2][0] = sin(psi)*sin(phi)+cos(psi)*cos(phi)*sin(theta);

   M[0][1] = sin(psi)*cos(theta);
   M[1][1] = cos(psi)*cos(phi)+sin(psi)*sin(theta)*sin(phi);
   M[2][1] = cos(theta)*sin(phi);

   M[0][2] = -sin(theta);
   M[1][2] = -cos(psi)*sin(phi)+sin(psi)*sin(theta)*cos(phi);
   M[2][2] = cos(theta)*cos(phi);
}
//calculates wanted position of platform attachment poins using calculated rotation matrix
//and translation vector\
//float pe[]
void getrxp()
{
   for(int i=0;i<6;i++){
      rxp[0][i] = T[0]+M[0][0]*(re[0][i])+M[0][1]*(re[1][i])+M[0][2]*(re[2][i]);
      rxp[1][i] = T[1]+M[1][0]*(re[0][i])+M[1][1]*(re[1][i])+M[1][2]*(re[2][i]);
      rxp[2][i] = T[2]+M[2][0]*(re[0][i])+M[2][1]*(re[1][i])+M[2][2]*(re[2][i]);
   }
}
//function calculating translation vector - desired move vector + home translation vector
void getT(float pe[])
{
   T[0] = pe[0]+H[0];
   T[1] = pe[1]+H[1];
   T[2] = pe[2]+H[2];
}

unsigned char setPos(float pe[]){
    unsigned char errorcount;
    errorcount=0;
    for(int i = 0; i < 6; i++)
    {
        getT(pe);
        getmatrix(pe);
        getrxp();
        theta_a[i]=getAlpha(&i);
        if(i==INV1||i==INV2||i==INV3){
        //if(1){  
          ///NOTICE!!!! TODO THIS IS WHACKY. USED TO HAVE MINUS SIGN IN IF STATEMENT
          servo_pos[i] = constrain(zero[i] + (theta_a[i])*servo_mult, MIN,MAX);
        }
        else{
            servo_pos[i] = constrain(zero[i] + (theta_a[i])*servo_mult, MIN,MAX);
        }
    }

    for(int i = 0; i < 6; i++)
    {
        if(theta_a[i]==servo_min||theta_a[i]==servo_max||servo_pos[i]==MIN||servo_pos[i]==MAX){
            errorcount++;
        }
        servo[i].writeMicroseconds(servo_pos[i]);
        //Serial.print(servo_pos[0]); //print to monitor for hardware in-loop test
        //Serial.print("\n");
    }
    return errorcount;
}


//void retPos(){
//   for(int i=0;i<6;i++){
//       long val;
//       if(i<3){
//           val=(long)(arr[i]);
//       }else{
//           val=(long)(arr[i]);
//       }
//       Serial.write(val);
//       Serial.write((val>>8));
//       Serial.write((val>>16));
//       Serial.write((val>>24));
//       Serial.flush();
//   }
//}


static inline int8_t sgn(float val) {
 if (val < 0) return -1;
 if (val==0) return 0;
 return 1;
}
