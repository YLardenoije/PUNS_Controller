#include <Arduino.h>

// put function declarations here:
void setup() {
  // Initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}

void loop() {
  // Check if data is available to read
  String string = "";
  while (Serial.available() > 0) {
    // Read the incoming byte:
    char incomingByte = Serial.read();
    string+=incomingByte;
    
    // Echo the incoming byte back to the serial output:
    
  }
  if (string != "") {
    Serial.println(string);
  }
}