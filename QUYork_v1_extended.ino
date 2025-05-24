#include "Adafruit_DRV2605.h" // Library for DRV2605 motor driver

#define TCAADDR 0x70 // Multiplexer address

// Global variables for vibration settings
int selectedMotor = -1; // No motor selected initially
int motorStrength[3] = {0x00, 0x00, 0x00}; // Motor strengths for motors 0, 1, and 2
int motorDuration = 200; // Vibration duration in milliseconds (default 0.2 seconds)
//String vibrationStrengthName[3] = {"No vibration", "No vibration", "No vibration"}; // Vibration strength names for motors 0, 1, and 2
uint8_t vibrationStrenth = 0; // do we need this at all? we can just set the int motorStrength directly...

// Motor driver variable
Adafruit_DRV2605 drv;

// Select the port on the multiplexer
void tcaselect(uint8_t i) {
  if (i > 2) return; // Select motors 0, 1, or 2

  Wire.beginTransmission(TCAADDR);
  Wire.write(1 << i);
  Wire.endTransmission();
}

// Initialize motor driver for the specified port
void initialize(int n) {
  tcaselect(n);
  drv.begin();
  if (!drv.begin()) {
    Serial.println("Could not find DRV2605");
  }
  drv.setMode(DRV2605_MODE_REALTIME);
}

// Vibration function
void buzz(int di1, int strength) {
  tcaselect(di1);
  drv.setRealtimeValue(strength);
  delay(motorDuration); // Vibration duration
  drv.setRealtimeValue(0x00); // Stop vibration
}

void buzz2(int di1, int strength,int di2, int strength2) {
  tcaselect(di1);
  drv.setRealtimeValue(strength);
  tcaselect(di2);
  drv.setRealtimeValue(strength2);
  delay(motorDuration); // Vibration duration
  drv.setRealtimeValue(0x00); // Stop vibration
  tcaselect(di1);
  drv.setRealtimeValue(0x00);
}

void setup() {
  // Initialize serial communication
  Serial.begin(115200);
  while (!Serial);

  // Clear Serial Monitor
  for (int i = 0; i < 10; i++) {
    Serial.println();
  }

  // Initialize I2C communication
  Wire.begin();

  // Initialize the motor driver ports
  for (int i = 0; i < 2; i++) {
    initialize(i);
    Serial.print("Motor ");
    Serial.print(i);
    Serial.println(" initialized.");
  }

  // Send small vibration to both motors and print a helpful message
  buzz(0, 0x20);  // Changed to 0x20 for the smallest noticeable vibration
  buzz(1, 0x20);  // Changed to 0x20 for the smallest noticeable vibration

  // User guide message
  Serial.println("Each command ends with a . (dot symbol)");
  Serial.println("1. Select motor: 'M0.', 'M1.', or 'M2.'");
  Serial.println("2. Set strength: 'S' followed by '0'-'128' (e.g., 'S53.' for medium-low vibration)");
  Serial.println("3. Set duration: 'D' followed by miliseconds (e.g., 'D400.' for 0.4 seconds)");
  Serial.println("4. Run motor: 'G' followed by motor number (e.g., 'G1.' to run motor 1)");
  Serial.println("S0. is no vibration, G2. activates both motors");
}

void loop() {
  static unsigned long lastInputTime = 0; // To track last input time
  unsigned long currentTime = millis(); // Get the current time
  
  // Check for manual input
  if (Serial.available() > 0) {
    // char input = Serial.read();
    String input = Serial.readStringUntil('.');

//    Serial.print("input: ");
//    Serial.println(input);

    if (input.indexOf('M') >= 0)
    {
      input.remove(0,1); // index 0, remove 1 char
//      Serial.print("use motor: ");
//      Serial.println(input);

      selectedMotor = input.toInt();

      Serial.print("Set motor: ");
      Serial.print(selectedMotor);
      Serial.print(", Strength: ");
      Serial.print(motorStrength[selectedMotor]);
      Serial.print(", Duration: ");
      Serial.print(motorDuration);
      Serial.println(" ms");

      
    }
    

    if (input.indexOf('S') >= 0)
    {
      input.remove(0,1); // index 0, remove 1 char
//      Serial.print("use strength: ");
//      Serial.println(input);

      motorStrength[selectedMotor] = input.toInt();

      Serial.print("Set motor: ");
      Serial.print(selectedMotor);
      Serial.print(", Strength: ");
      Serial.print(motorStrength[selectedMotor]);
      Serial.print(", Duration: ");
      Serial.print(motorDuration);
      Serial.println(" ms");
      
    }
    




    if (input.indexOf('D') >= 0)
    {
      input.remove(0,1); // index 0, remove 1 char
//      Serial.print("use duration: ");
//      Serial.println(input);

      motorDuration = input.toInt();

      Serial.print("Set motor: ");
      Serial.print(selectedMotor);
      Serial.print(", strength: ");
      Serial.print(motorStrength[selectedMotor]);
      Serial.print(", duration: ");
      Serial.print(motorDuration);
      Serial.println(" ms");

    }

    



    if (input.indexOf('G') >= 0)
    {
      input.remove(0,1); // index 0, remove 1 char
      // printing takes time, for faster responses of the device, just buzz right away

      int runmotor = input.toInt();

      if (runmotor == 2)
      {
        
        buzz2(0, motorStrength[2], 1, motorStrength[2]);
        
      } else {

        buzz(runmotor, motorStrength[runmotor]);
        
      }

      Serial.print("Activated motor: ");
      Serial.print(selectedMotor);
      Serial.print(", Strength: ");
      Serial.print(motorStrength[selectedMotor]);
      Serial.print(", Duration: ");
      Serial.print(motorDuration);
      Serial.println(" ms");


      
    }


    lastInputTime = currentTime;  // Update last input time
  }

  // Check if no manual input for 30 seconds, print 'System Standby'
  if (currentTime - lastInputTime >= 30000) {
    Serial.println("System Standby");
    lastInputTime = currentTime;  // Reset the last input time
  }

  delay(8); // Small delay to prevent high CPU usage
  // changed delay to half a frame in the psychopy setup (60 Hz monitor)
}
