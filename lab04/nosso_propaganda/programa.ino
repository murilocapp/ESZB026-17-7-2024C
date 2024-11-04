int potPin = A0;  
int valorPot;

void setup(){
   // Configura a serial: baud rate de 115200, 8-bit, sem paridade, 1 stop bit
   Serial.begin(115200, SERIAL_8N1);
}

void loop() {
  valorPot = analogRead(potPin);  // Lê o valor do potenciômetro
  Serial.println(valorPot);        // Envia o valor para a Raspberry Pi
  delay(1000);                       
}
