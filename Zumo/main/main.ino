#include <Wire.h>
#include <Zumo32U4.h>
#include <time.h>

int toNicla = 13;
int fromNicla = 14;

Zumo32U4Motors motors;
Zumo32U4ButtonB buttonB;
Zumo32U4OLED display;
Zumo32U4Buzzer buzzer;

const char fugue[] PROGMEM =
  "! O5 L16 agafaea dac+adaea fa<aa<bac#a dac#adaea f"
  "O6 dcd<b-d<ad<g d<f+d<gd<ad<b- d<dd<ed<f+d<g d<f+d<gd<ad"
  "L8 MS <b-d<b-d MLe-<ge-<g MSc<ac<a ML d<fd<f O5 MS b-gb-g"
  "ML >c#e>c#e MS afaf ML gc#gc# MS fdfd ML e<b-e<b-"
  "O6 L16ragafaea dac#adaea fa<aa<bac#a dac#adaea faeadaca"
  "<b-acadg<b-g egdgcg<b-g <ag<b-gcf<af dfcf<b-f<af"
  "<gf<af<b-e<ge c#e<b-e<ae<ge <fe<ge<ad<fd"
  "O5 e>ee>ef>df>d b->c#b->c#a>df>d e>ee>ef>df>d"
  "e>d>c#>db>d>c#b >c#agaegfe f O6 dc#dfdc#<b c#4";

void setup()
{
  Wire.begin();
  Serial.begin(115200);
  pinMode(toNicla, OUTPUT);      
  pinMode(fromNicla, INPUT_PULLUP);

  display.clear();
  display.print(F("test"));

  // Wait for the user to press button A.
  //buttonB.waitForButton();
  Serial.println("Booted");

  // Delay so that the robot does not move away while the user is
  // still touching it.
  delay(1000);
  //buzzer.playFromProgramSpace(fugue);
  buzzer.playFrequency(440, 200, 15);
  display.clear();
}

int drive(int velocity, int yaw)
{
  int L, R, deltaV; 
  static int lastYaw;

  deltaV = yaw / 2 + 3 * (yaw - lastYaw);
  lastYaw = yaw;

  L = velocity + deltaV;
  R = velocity - deltaV;
  motors.setSpeeds(L, R);

  display.clear();
  display.gotoXY(0,0);
  display.print(L);
  display.gotoXY(0,1);
  display.print(R);
  return 0;
}

// reverses the inputs bits
unsigned int reverseBits(uint8_t num) {
    unsigned int reversed = 0;
    unsigned int bitCount = sizeof(num) * 8; // Get the total number of bits in the number

    for (unsigned int i = 0; i < bitCount; ++i) {
        if (num & (1 << i)) {
            reversed |= 1 << ((bitCount - 1) - i);
        }
    }

    return reversed;
}

int readData() {
  unsigned int speed = 0;
  bool lastValue;

  //Serial.println("Reading data from Nicla...");

  // Check for start bit (high-low transition)
  if (!digitalRead(fromNicla)) {
    delay(5);
    if (digitalRead(fromNicla)) { // Ensure start bit is stable
      Serial.println("Start bit detected");
    } else {
      //Serial.println("Error: Start bit not detected");
      return -128;
    }
  } else {
    //Serial.println("Error: Missing start bit");
    return -128;
  }

  // Read 8 data bits (LSB first)
  for (int i = 0; i < 9; i++) {
    delay(5);
    lastValue = !digitalRead(fromNicla); // Read current pin state
    Serial.print("Bit ");
    Serial.print(i);
    Serial.print(": ");
    Serial.println(lastValue);
    if(i == 8 && lastValue !=1)
      return -128;
    else if(i == 8)
      break;
    else
      speed = (speed << 1) | lastValue;// Shift speed left and add current bit value (1 for high, 0 for low)
  }
  
  unsigned int MSB = reverseBits(speed); // reverse bits to get the number in MSB order
  int signedMSB;

  
  if (MSB > 128) {
    signedMSB = -((~MSB + 1) & 0xFF); // Corrected to handle negative conversion properly
  } else {
    signedMSB = MSB;
  }

  if(signedMSB > 100) // correct the number to something more realistic. Possibly change this for a non blocking error.
    signedMSB = signedMSB - 100;
  else if(signedMSB < -100)
    signedMSB = signedMSB + 100;

  Serial.print("Received value (Converted to MSB first): ");
  Serial.println(signedMSB);
  //display.clear();
  //display.print(signedMSB);
  return signedMSB;
}

void loop()
{
  int i = 0;
  int dt = 0;
  int yaw, velocity, e;
  ledYellow(1);
  /*while(1)
  {
    e = drive(100, 100);
  }*/
  while(1)
  {
    dt = millis();

    do
      i = readData();
    while(i == -128);

    if((millis()-dt) > 120) // if the delay is over 80 ms it must be the yaw
      yaw = i;
    else
      velocity = i;   
    /*display.clear();
    display.gotoXY(0,0);
    display.print(velocity);
    display.gotoXY(0,1);
    display.print(yaw);*/
    //e = drive(velocity, yaw);  
  }
  //delay(1000);
}