
#include <Servo.h>

// This example demonstrates CmdMessenger's callback  & attach methods
// For Arduino Uno and Arduino Duemilanove board (may work with other)

// Download these into your Sketches/libraries/ folder...

// CmdMessenger library available from https://github.com/dreamcat4/cmdmessenger
#include <CmdMessenger.h>

// Base64 library available from https://github.com/adamvr/arduino-base64
#include <Base64.h>

// Streaming4 library available from http://arduiniana.org/libraries/streaming/
#include <Streaming.h>

// Mustnt conflict / collide with our message payload data. Fine if we use base64 library ^^ above
char field_separator = ',';
char command_separator = ';';
Servo myServo;
int numServos = 5;
Servo servoObjs[5];
int pins[5];
int startPositions[5];
int endPositions[5];
int gateTime = 10000;

// Attach a new CmdMessenger object to the default Serial port
CmdMessenger cmdMessenger = CmdMessenger(Serial, field_separator, command_separator);


// ------------------ C M D  L I S T I N G ( T X / R X ) ---------------------

// We can define up to a default of 50 cmds total, including both directions (send + recieve)
// and including also the first 4 default command codes for the generic error handling.
// If you run out of message slots, then just increase the value of MAXCALLBACKS in CmdMessenger.h

// Commands we send from the Arduino to be received on the PC
enum
{
  kCOMM_ERROR    = 000, // Lets Arduino report serial port comm error back to the PC (only works for some comm errors)
  kACK           = 001, // Reports acknowledgment of command
  kARDUINO_READY = 002,
  kERR           = 003, // Arduino reports badly formatted cmd, or cmd not recognised

  // Now we can define many more 'send' commands, coming from the arduino -> the PC, eg
  // kICE_CREAM_READY,
  // kICE_CREAM_PRICE,
  // For the above commands, we just call cmdMessenger.sendCmd() anywhere we want in our Arduino program.

  kSEND_CMDS_END, // Mustnt delete this line
};

// Commands we send from the PC and want to recieve on the Arduino.
// We must define a callback function in our Arduino program for each entry in the list below vv.
// They start at the address kSEND_CMDS_END defined ^^ above as 004
messengerCallbackFunction messengerCallbacks[] = 
{
  setServoStartPosition,         // 004
  setServoEndPosition,    // 005
  getStartPosition,              // 006
  getEndPosition,         // 007
  NULL
};
// Its also possible (above ^^) to implement some symetric commands, when both the Arduino and
// PC / host are using each other's same command numbers. However we recommend only to do this if you
// really have the exact same messages going in both directions. Then specify the integers (with '=')


// ------------------ C A L L B A C K  M E T H O D S -------------------------

/**
 *Set the start position of a specific servo
 *INPUT:
 *First Valuee: Servo to set
 *Second Value: Servo Start Angle 
 **/
void setServoStartPosition()
{
 String response = "";
 char buf[350] = {'\0'};
 cmdMessenger.copyString(buf, 350);
 if(buf[0] == '\0')
  {
     cmdMessenger.sendCmd(kERR, "");
     return;
  }
  response += buf;
  response += ",";
  int s = atoi(buf);
  cmdMessenger.copyString(buf, 350);
  if(buf[0] == '\0')
    {
       cmdMessenger.sendCmd(kERR, "");
       return; 
    }
   response += buf;
   startPositions[s] = atoi(buf);
   char responseChars[response.length()+1];
   response.toCharArray(responseChars, response.length()+1);
   cmdMessenger.sendCmd(kACK, responseChars);
}

 /**
 *Set the end position of a specific servo
 *INPUT:
 *First Valuee: Servo to set
 *Second Value: Servo End Angle 
 **/
void setServoEndPosition()
{
 String response = "";
 char buf[350] = {'\0'};
 cmdMessenger.copyString(buf, 350);
 if(buf[0] == '\0')
  {
     cmdMessenger.sendCmd(kERR, "");
     return;
  }
  response += buf;
  response += ",";
  int s = atoi(buf);
  cmdMessenger.copyString(buf, 350);
  if(buf[0] == '\0')
    {
       cmdMessenger.sendCmd(kERR, "");
       return; 
    }
   response += buf;
   endPositions[s] = atoi(buf);
   char responseChars[response.length()+1];
   response.toCharArray(responseChars, response.length()+1);
   cmdMessenger.sendCmd(kACK, responseChars);
}


/**
 *Gets the start position of a certain servo
 *INPUT:
 *First Value: Servo to query
 *OUTPUT: Start angle of the servo
 *First Value: Servo queried
 **/
void getStartPosition()
{
  String response = "";
  char buf[350] = { '\0'};
  //Get first value
  cmdMessenger.copyString(buf, 350);
  if(buf[0] == '\0') 
  {
    cmdMessenger.sendCmd(kERR, "");
    return;
  }
  response += buf;
  response += ",";
  int thePosition = startPositions[atoi(buf)];
  response += String(thePosition);
  char responseChars[response.length()+1];
  response.toCharArray(responseChars, response.length()+1);
  cmdMessenger.sendCmd(kACK, responseChars);
}

/**
 *Gets the end position of a certain servo
 *INPUT:
 *First Value: Servo to query
 *OUTPUT: End angle of the servo
 *First Value: Servo queried
 **/
void getEndPosition()
{
  String response = "";
  char buf[350] = { '\0'};
  //Get first value
  cmdMessenger.copyString(buf, 350);
  if(buf[0] == '\0') 
  {
    cmdMessenger.sendCmd(kERR, "");
    return;
  }
  response += buf;
  response += ",";
  int thePosition = endPositions[atoi(buf)];
  response += String(thePosition);
  char responseChars[response.length()+1];
  response.toCharArray(responseChars, response.length()+1);
  cmdMessenger.sendCmd(kACK, responseChars);
}



// ------------------ D E F A U L T  C A L L B A C K S -----------------------

void arduino_ready()
{
  // In response to ping. We just send a throw-away Acknowledgement to say "im alive"
  cmdMessenger.sendCmd(kACK,"Arduino ready");
}

void unknownCmd()
{
  // Default response for unknown commands and corrupt messages
  cmdMessenger.sendCmd(kERR,"Unknown command");
}

// ------------------ E N D  C A L L B A C K  M E T H O D S ------------------



// ------------------ S E T U P ----------------------------------------------

void attach_callbacks(messengerCallbackFunction* callbacks)
{
  int i = 0;
  int offset = kSEND_CMDS_END;
  while(callbacks[i])
  {
    cmdMessenger.attach(offset+i, callbacks[i]);
    i++;
  }
}

void setup() 
{
  // Listen on serial connection for messages from the pc
  Serial.begin(115200); // Arduino Uno, Mega, with AT8u2 USB

  // cmdMessenger.discard_LF_CR(); // Useful if your terminal appends CR/LF, and you wish to remove them
  cmdMessenger.print_LF_CR();   // Make output more readable whilst debugging in Arduino Serial Monitor

  // Attach default / generic callback methods
  cmdMessenger.attach(kARDUINO_READY, arduino_ready);
  cmdMessenger.attach(unknownCmd);

  // Attach my application's user-defined callback methods
  attach_callbacks(messengerCallbacks);

  arduino_ready();
  for(int i = 0; i < numServos; ++i)
  {
    servoObjs[i].attach(pins[i]);
    pins[i] = 13-i;
    startPositions[i] = 0;
    endPositions[i] = 0;
  }
}


void loop() 
{
  // Process incoming serial data, if any
  cmdMessenger.feedinSerialData();
  // Loop
  for(int i = 0; i < numServos; ++i)
  {
    servoObjs[i].write(startPositions[i]);
  }
  delay(gateTime);
  for(int i = 0; i < numServos; ++i)
  {
    servoObjs[i].write(startPositions[i]);
  }
}


