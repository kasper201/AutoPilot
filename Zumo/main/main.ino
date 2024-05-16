#include <Wire.h>
#include <Zumo32U4.h>

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
  buttonB.waitForButton();
  Serial.println("Booted");

  // Delay so that the robot does not move away while the user is
  // still touching it.
  delay(1000);
  //buzzer.playFromProgramSpace(fugue);
  buzzer.playFrequency(440, 200, 15);
  display.clear();
}

void readData()
{
  int speed = 0;
  bool tmp;
  if(digitalRead(fromNicla))
  {
    delay(3);
    if(!digitalRead(fromNicla)) // if not matched, stop
      return;
    delay(2);

    for(int i = 0; i <= 9; i++)
    {
      Serial.print("fromNicla value1: ");
      Serial.println(digitalRead(fromNicla));

      delay(2);
      tmp = digitalRead(fromNicla);
      Serial.print("fromNicla value2: ");
      Serial.println(digitalRead(fromNicla));

      delay(2);
      Serial.print("fromNicla value3: ");
      Serial.println(digitalRead(fromNicla));
        if(tmp == digitalRead(fromNicla))
        {
          if(digitalRead(fromNicla)) 
            1 >> speed;
          else
            0 >> speed;
        }
        else
          Serial.println("OHNO");
      delay(1);
    }
    Serial.print("Entered value is: ");
    Serial.println(speed);
  }
}

void loop()
{
  ledYellow(1);
  display.clear();
  //display.print(F("2"));
  //display.gotoXY(i,1);
  //display.print(speed[i]);
  readData();
  delay(1000);
}