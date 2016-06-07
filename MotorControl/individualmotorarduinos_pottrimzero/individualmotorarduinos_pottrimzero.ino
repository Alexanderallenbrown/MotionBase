// Assign your channel in pins
#define CHANNEL_A_PIN 2
#define CHANNEL_B_PIN 3
volatile long unCountShared;

//A0 reads in angle
//0-5V = 0-pi
const int analogInPin=A0;
const int analogOutPin1=11;
const int analogOutPin2=9;
const int analogOutPin3=10;

float k_pot = (320.0)/(PI/2);

int deadBand = 50;

int val = 0; 
int val2 = 0;
int mag = 0;

static int globzeros[6] = {140,414,700,499,448,457};
static float motorsigns[6] = {1.0,-1.0,1.0,-1.0,1.0,-1.0};
static int zero[6]={1475,1470,1490,1480,1460,1490}; //Zero positions of servos

// ONLY USE ARDUINO 2:1.0.5 WITH THIS CODE DO NOT USE OLD VERSION

//put the motor number for this arduino here:
int motornum = 1;

int glob0 = globzeros[motornum-1];

# define PWM_SOURCE 7
float servo_mult=1000.0/(PI);

float ref_command_float = 0;
int rawpos;
float posfloat;

boolean jogmode=false;

void setup()
{
  Serial.begin(115200);
  //attach the interrupts
  //attachInterrupt(0, channelA,CHANGE);
  //attachInterrupt(1, channelB,CHANGE);
  pinMode(analogOutPin2,OUTPUT);
  pinMode(analogOutPin3,OUTPUT);
  //attachInterrupt(0, channelA,CHANGE);
  //attachInterrupt(1, channelB,CHANGE);
//  int tot = 0;
//  for (int k=0; k<100; k++){
//    tot += analogRead(1);
//    delay(1);
//  }
//  int globV = tot/100;
  int globV = analogRead(1);
  Serial.print(globV);
  Serial.print('\t');
  int glob0 = 100;
  //float k_pot = (390.0-100.0)/(PI/4);
  float globPos = (globV - glob0)/k_pot;
  Serial.print(globPos);
  Serial.print('\t');
  unCountShared = long( globPos*8000/(2*PI) );
  Serial.print(unCountShared);
  Serial.print('\t');
  delay(1000);
}

void loop()
{
  // create local variables to hold a local copies of the channel inputs
  // these are declared static so that thier values will be retained
  // between calls to loop.
  //static long unCount;
        	
  //noInterrupts(); // turn interrupts off quickly while we take local copies of the shared variables

  //unCount = unCountShared;
  if (jogmode==false){
   // static long unCount;
        	
   // noInterrupts(); // turn interrupts off quickly while we take local copies of the shared variables

    //unCount = unCountShared;
 
    //interrupts(); 
  
    //float posfloat = unCount*2*PI/(8000.0); //our encoder position in radians
    rawpos = analogRead(1);
    posfloat = motorsigns[motornum-1]*(rawpos - glob0)/k_pot;
    //val is desired angle
    //0-1023 = 0-pi
    //val = analogRead(analogInPin); //raw reference position value.
    //val = val-512; //this number should be scaled to go from -PI to PI
    val = pulseIn(PWM_SOURCE, HIGH, 20000);
  
    //float ref_command_float = val*PI/512.0;//this should be the reference position in radians.
    ref_command_float = (val - zero[0])/servo_mult; //this should give the reference position, converted from microseconds to radians
  }
  
  else{
    //interrupts(); 
    rawpos = analogRead(1);
    posfloat = motorsigns[motornum-1]*(rawpos - glob0)/k_pot;
    val = analogRead(analogInPin); //raw reference position value.
    val=val-512; //this number should be scaled to go from -PI to PI
  
    ref_command_float = val*PI/512.0;//this should be the reference position in radians.
  }
  
  if (ref_command_float>PI/2){
    ref_command_float = PI/2;
  }
  if (ref_command_float<0){
    ref_command_float = 0;
  }
  
  float float_error = ref_command_float-posfloat;//this is our current error value!!
  
  float kp = 255.0/(PI/6.0);//some guess for KP.........
  
  float float_U = kp*float_error;
  
  if(float_U>255.0){
    float_U = 255.0;
  }
  
  if (float_U<-255.0){
    float_U = -255.0;
  }
  
  val2 = int(float_U);
  mag = abs(val2);

  if(val2>deadBand){
    //Serial.print("!!!!!!!!!!!!");
   digitalWrite(analogOutPin3,HIGH);
   analogWrite(analogOutPin1,mag);
   digitalWrite(analogOutPin2,LOW);
 }
 else if(val2<-deadBand){
   digitalWrite(analogOutPin2,HIGH);
   analogWrite(analogOutPin1,mag);
   digitalWrite(analogOutPin3,LOW);
 }
 
 else{
   digitalWrite(analogOutPin3,LOW);
   analogWrite(analogOutPin1,0);
   digitalWrite(analogOutPin2,LOW);
 }
 
  Serial.print(posfloat);
  Serial.print("\t");
  Serial.print(ref_command_float);
  Serial.print("\t");
  Serial.print(rawpos);
  Serial.print("\t");
  Serial.print(float_error);
  Serial.print("\t");
  Serial.print(float_U);
  Serial.print("\t");
  Serial.print(val2);
  Serial.print("\t");
  Serial.println(mag);
  
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
