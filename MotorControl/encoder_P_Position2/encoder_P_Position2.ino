// Assign your channel in pins
#define CHANNEL_A_PIN 2
#define CHANNEL_B_PIN 3
volatile long unCountShared;

//A0 reads in angle
//0-5V = 0-pi
const int analogInPin=A0;
const int analogOutPin1=4;
const int analogOutPin2=5;
const int analogOutPin3=6;

int val = 0; 
int val2 = 0;
int mag = 0;
//float servo_mult=0;

# define PWM_SOURCE 7
static int zero[6]={1475,1470,1490,1480,1460,1490}; //Zero positions of servos, in this positions their arms are perfectly horizontal, in us
float servo_mult=400.0/(PI/4);

void setup()
{
  Serial.begin(115200);
  //attach the interrupts
  attachInterrupt(0, channelA,CHANGE);
  attachInterrupt(1, channelB,CHANGE);
}
void loop()
{
  // create local variables to hold a local copies of the channel inputs
  // these are declared static so that their values will be retained
  // between calls to loop.
  static long unCount;
        	
  noInterrupts(); // turn interrupts off quickly while we take local copies of the shared variables

  unCount = unCountShared;
 
  interrupts(); 
  
  float posfloat = unCount*2*PI/(8000.0); //our encoder position in radians
  //val is desired angle
  //0-1023 = 0-pi
  //val = analogRead(analogInPin); //raw reference position value.
  //val = val-512; //this number should be scaled to go from -PI to PI
  val = pulseIn(PWM_SOURCE, HIGH, 20000);
  
  //float ref_command_float = val*PI/512.0;//this should be the reference position in radians.
  float ref_command_float = zero[0] - val/servo_mult; //this should give the reference position, converted from microseconds to radians
  
  float float_error = ref_command_float - posfloat;//this is our current error value!!
  
  float kp = 100.0/(PI/4.0);//some guess for KP.........
  
  float float_U = kp*float_error;
  
  if(float_U>255.0){
    float_U = 255.0;
  }
  
  if (float_U<-255.0){
    float_U = -255.0;
  }
  
  val2 = int(float_U);
  mag = abs(val2);

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
  Serial.print("\n");
  Serial.print(ref_command_float);
  Serial.print("\n");
//  Serial.print(posfloat);
//  Serial.print("\t");
//  Serial.print(float_error);
//  Serial.print("\t");
//  Serial.print(float_U);
//  Serial.print("\t");
//  Serial.print(val2);
//  Serial.print("\t");
//  Serial.println(mag);
  
//  Serial.println(val);
//  Serial.println(mag);
//  Serial.print(millis());
//  Serial.print("\t");
//  Serial.println(unCount);
  delay(1);
  
}


// simple interrupt service routine
void channelA()
{
  //Serial.println("A");
  if (digitalRead(CHANNEL_A_PIN) == HIGH)
  {
	if (digitalRead(CHANNEL_B_PIN) == LOW)
	{
  	unCountShared++;
	}
	else
	{
  	unCountShared--;
	}
  }
  else
  {
	if (digitalRead(CHANNEL_B_PIN) == HIGH)
	{
  	unCountShared++;
	}
	else
	{
  	unCountShared--;
	}
  }
}

void channelB()
{
  //Serial.println("B");
  if (digitalRead(CHANNEL_B_PIN) == HIGH)
  {
	if (digitalRead(CHANNEL_A_PIN) == HIGH)
	{
  	unCountShared++;
	}
	else
	{
  	unCountShared--;
	}
  }
  else
  {
	if (digitalRead(CHANNEL_A_PIN) == LOW)
	{
  	unCountShared++;
	}
	else
	{
  	unCountShared--;
	}
  }
}
