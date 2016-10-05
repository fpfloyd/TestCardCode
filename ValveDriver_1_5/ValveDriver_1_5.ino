/*

 Code for driving solenoid pumps for functionalization rig.
 
 Assumes solenoids are connected on digital pins 2-10. Uses internal pull-ups on those pins.
 
 - Connects to serial port.
 - Expects commands of the form: "x,y" where X is a pin number (2-10) and Y is a 0 or 1. If "q" is received,
 - A command "S" returns state of sentry pins
 
 Aaron Oppenheimer
 Daktari Diagnostics
 
 ChangeLog
 20120727  Initial work
 20120821  Updated string parsing so we can request sentry state and for future flexibility
 20120823  v1.3  Changed to use analog input. Assumes external pullup (~1MΩ).
 20120907  v1.4  Changed to return entire analog value; will parse on PC.
 20121024  v1.5  Stripped out the sentry pin stuff, since we've moved to the impedance meter
 
 */



// pins for the solenoids:
const int firstPin = 2;
const int lastPin = 11;

const int hist=10;

int ledVal=0;

int s1, lasts1;
int s2, lasts2;

String readString = String(8);
char readChar;
String vstr, sstr;
int v,s;
char carray[6];

void setup() {
  // initialize serial:
  Serial.begin(9600);
  // make the pins outputs:

  for (int i = firstPin; i <= lastPin; i++) {
    pinMode(i, OUTPUT); 
    digitalWrite(i, LOW); // turn off the pin by default, so the solenoid will not be energized
  }

  readString="";
  Serial.println("Version 1.5");

  Serial.println("\nGO");
}

void loop() {

  if(Serial.available()>0) {
    // check if there is charecter in the serial buffer
    readChar=Serial.read(); // read the serial data which is charecter store it in p

    if (readChar=='\r') {
      // end of string, so parse it

      if (readString.length()>0) {
        // should be a string of the form XX,Y where XX is the valve number and Y is the state - 0 or 1. XX can be one or two digits long
        vstr = readString.substring(0,readString.length()-2);
        vstr.toCharArray(carray,sizeof(carray));
        v=atoi(carray);

        sstr = readString.substring(readString.length()-1,readString.length());
        sstr.toCharArray(carray,sizeof(carray));
        s=atoi(carray);

        updatePin(v,s);
      }

      readString="";
    }
    else {     
      readString += String(readChar);
    }
  }

}

void updatePin(int inpin, int inval) {
  // OK - is the pin number valid?
  if (inpin >= firstPin && inpin <= lastPin) {
    if (inval == 0) {
      digitalWrite(inpin, LOW);
    } 
    else {
      digitalWrite(inpin, HIGH);
    }
    Serial.println("OK");
  } 
  else {
    // ignore. should probably return an error instead
    Serial.print("Error - Pin not OK:");
    Serial.println(inpin);
  }
}






