const int pingPin = 6; // Trigger Pin of Ultrasonic Sensor
const int echoPin = 7;// Echo Pin of Ultrasonic Sensor

//motor driver pins
const int enA = 5; //right motor
const int enB = 3; //left motor
const int in1 = 11;
const int in2 = 10;
const int in3 = 9;
const int in4 = 8;

//For pwm control of motors
int maximumPwm = 100;
float LPwmGain = 0.9;
float turnConst = 0.3; //for the pwm gain of inner wheel while turning. 1 means no change in pwm
float turnGain = 1.2; //the motors are having trouble turning, so more power needs to be sent to the motors while turning. 1 means *1

//Random variables
const int ledPin = 4;
long duration;
int cm;
int incomingByte =0;


//max length of object in the front in cm
float maxlengthObj = 14;

//Check if sonar will be active
boolean sonarCheck=false;


void setup() {
  Serial.begin(9600);

  pinMode(ledPin, OUTPUT);
  
  // Set all the motor control pins to outputs
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  
  // Turn off motors - Initial state
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);

  // Ultrasonic sensor
  pinMode(pingPin,OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  cm = sonarL();
  if (cm<=maxlengthObj){
      stopCar();
      digitalWrite(ledPin, HIGH);
  }
  else{
    digitalWrite(ledPin, LOW);
    if (Serial.available() > 0){
      incomingByte = Serial.read();
      if (incomingByte == 'f'){
        forward();
        //delay(500);
      }
      if (incomingByte == 'R'){
        reverse();
        //delay(500);
      }
      if (incomingByte == 'l'){
        left();
        //delay(500);
      }
      if (incomingByte == 'r'){
        right();
        //delay(500);
      }
      if (incomingByte == 'x'){
        stopCar();
        delay(500);
      }
    }
  }
}

long sonarL(){
  digitalWrite(pingPin, LOW);
  delayMicroseconds(2);
  digitalWrite(pingPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(pingPin, LOW);
  pinMode(echoPin, INPUT);
  duration = pulseIn(echoPin, HIGH);
  cm = microsecondsToCentimeters(duration);
  return cm;
}

long microsecondsToCentimeters(long microseconds) {
   return microseconds / 29 / 2;
}

void forward() {
  analogWrite(enA, maximumPwm);
  analogWrite(enB, maximumPwm*LPwmGain);

  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  
}

void reverse() {
  analogWrite(enA, maximumPwm);
  analogWrite(enB, maximumPwm*LPwmGain);

  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
} 

void stopCar() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
} 

void left() {
  analogWrite(enA, maximumPwm*turnGain);
  analogWrite(enB, maximumPwm*LPwmGain*turnConst);

  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
} 

void right() {
  analogWrite(enA, maximumPwm*turnConst);
  analogWrite(enB, maximumPwm*LPwmGain*turnGain);

  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
} 
