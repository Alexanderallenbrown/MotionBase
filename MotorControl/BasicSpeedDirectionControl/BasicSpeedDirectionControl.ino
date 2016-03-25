const int analogInPin=A0;
const int analogOutPin1=9;
const int analogOutPin2=10;
const int analogOutPin3=11;




void setup(){

Serial.begin(9600);
}

void loop(){
  
int val = analogRead(analogInPin); 
int val2 = val-512;
int mag = abs(val2*255/512);
  
 if(val2<0){
   analogWrite(10,0);
   analogWrite(9,mag);
   analogWrite(11,255);
 }
 else{
   analogWrite(11,0);
   analogWrite(9,mag);
   analogWrite(10,255);
 }
}

