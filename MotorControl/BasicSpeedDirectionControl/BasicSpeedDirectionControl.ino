const int analogInPin=A0;
const int analogOutPin1=9;
const int analogOutPin2=10;
const int analogOutPin3=11;

int val = 0; 
int val2 = 0;
int mag = 0;


void setup(){

Serial.begin(9600);
}

void loop(){
  
val = analogRead(analogInPin); 
val2 = val-512;
mag = abs(val2*(255/512));
  
 if(val2<0){
   analogWrite(analogOutPin2,0);
   analogWrite(analogOutPin1,mag);
   analogWrite(analogOutPin3,255);
 }
 else{
   analogWrite(analogOutPin3,0);
   analogWrite(analogOutPin1,mag);
   analogWrite(analogOutPin2,255);
 }
 Serial.println(val);
 Serial.println(mag);
 
 delay(2);
}

