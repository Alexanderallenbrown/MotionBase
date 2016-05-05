const int analogInPin=A0;
const int analogOutPin1=11;
const int analogOutPin2=9;
const int analogOutPin3=10;

int val = 0; 
int val2 = 0;
int mag = 0;


void setup(){

Serial.begin(115200);
}

void loop(){
  
val = analogRead(analogInPin); 
val2 = val-512;
mag = abs(val2/2);
if(mag>255){
  mag = 255;
}
else{
  mag = mag;
}
  
 if(val2<-20){
   digitalWrite(analogOutPin2,LOW);
   analogWrite(analogOutPin1,mag);
   digitalWrite(analogOutPin3,HIGH);
 }
 else if(val2>20){
   digitalWrite(analogOutPin3,LOW);
   analogWrite(analogOutPin1,mag);
   digitalWrite(analogOutPin2,HIGH);
 }
 
 else{
   digitalWrite(analogOutPin3,LOW);
   analogWrite(analogOutPin1,0);
   digitalWrite(analogOutPin2,LOW);
 }
 
 Serial.print(val);
 Serial.print("\t");
 Serial.println(mag);
 
 delay(2);
}

