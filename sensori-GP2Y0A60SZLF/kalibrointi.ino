/*=========================================================
Written By Ville R. on 15.11.2020
===========================================================
*/
long sensorsum = 0;
int n = 1;
int distance = 10;
// How accurate the measurements are
int stepDistance = 5;
int mean = 0;


// The setup routine runs once when you press reset:
void setup() {
  // Initialize serial communication at 9600 bits per second:
  Serial.begin(9600);

  Serial.println("Beginning of measurements!");
    // Wait for 10 seconds before beginning the measurements
  delay(10000);
}

// The loop routine runs over and over again forever:
void loop() {
  
  // Read the input on analog pin 0:
  int sensorValue = analogRead(A0);
 
  // Calculate mean of measures of a specified distance in order to smooth the results and after create the regression line for distance
  sensorsum = (sensorsum + sensorValue);
  mean = (sensorsum / n);
  n = n + 1;

  // 500 measurements are made
  if (n > 500) {
    // Print the information about the measurement
    Serial.println("-----RESET--------------------------------------------------------------------------------");
    Serial.print(distance);
    Serial.print(" cm: ");
    Serial.println(mean);
    distance = distance + 5;
    n = 1;
    sensorsum = 0;

    // Wait for 8 seconds to move the measurable object
    delay(8000);
  }

  // Measurement is done
  if (distance > 150) {
    nuku();
  }

  delay(25);
}

void nuku() {
  while(true){
    delay(10000);
  }
}
