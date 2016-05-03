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

float k_pot = (390-100)/(2*PI);

int val = 0; 
int val2 = 0;
int mag = 0;

static int globzeros[6] = {100,414,500,499,448,457};

//put the motor number for this arduino here:
int motornum = 1;

int glob0 = globzeros[motornum-1];

void setup()
{
  Serial.begin(115200);
  //attach the interrupts
  attachInterrupt(0, channelA,CHANGE);
  attachInterrupt(1, channelB,CHANGE);
  pinMode(analogOutPin2,OUTPUT);
  pinMode(analogOutPin3,OUTPUT);
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
  float k_pot = (390-100)/(2*PI);
  float globPos = (globV - glob0)/k_pot;
  Serial.print(globPos);
  Serial.print('\t');
  unCountShared = long( globPos*8000/(2*PI) );
  Serial.print(unCountShared);
  Serial.print('\t');
  delay(5000);
}

void loop()
{
  // create local variables to hold a local copies of the channel inputs
  // these are declared static so that thier values will be retained
  // between calls to loop.
  static long unCount;
        	
  noInterrupts(); // turn interrupts off quickly while we take local copies of the shared variables

  unCount = unCountShared;
 
  interrupts(); 
  
  //float posfloat = unCount*2*PI/(8000.0); //our encoder position in radians
  float posfloat = (analogRead(1) - glob0)/k_pot;
  //val is desired angle
  //0-1023 = 0-pi
  val = analogRead(analogInPin); //raw reference position value.
  val=val-512; //this number should be scaled to go from -PI to PI
  
  float ref_command_float = val*PI/512.0;//this should be the reference position in radians.
  
  float float_error = ref_command_float-posfloat;//this is our current error value!!
  
  float kp = 200.0/(PI/4.0);//some guess for KP.........
  
  float float_U = kp*float_error;
  
  if(float_U>255.0){
    float_U = 255.0;
  }
  
  if (float_U<-255.0){
    float_U = -255.0;
  }
  
  val2 = int(float_U);
  mag = abs(val2);

  if(val2>40){
    Serial.print("!!!!!!!!!!!!");
   digitalWrite(analogOutPin3,HIGH);
   analogWrite(analogOutPin1,mag);
   digitalWrite(analogOutPin2,LOW);
 }
 else if(val2<-40){
   digitalWrite(analogOutPin2,HIGH);
   analogWrite(analogOutPin1,mag);
   digitalWrite(analogOutPin3,LOW);
 }
 
 else{
   digitalWrite(analogOutPin3,LOW);
   analogWrite(analogOutPin1,0);
   digitalWrite(analogOutPin2,LOW);
 }
 
  Serial.print(analogRead(1));
  Serial.print("\t");
  Serial.print(ref_command_float);
  Serial.print("\t");
  Serial.print(unCount);
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
