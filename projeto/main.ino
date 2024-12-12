const int ledPin = 2; //pino digital de saida do led
const int micPin = A0; //pino do microfone 
int ledState = 0; //inicia com led desligado
int iniciaColeta = 0; //variavel de estado da coleta
int loopDelay = 1000;
char charRecebido;

void alarm(int bips = 4, int interval = 100) {
    for (int i = 0; i < bips; i++) {
        digitalWrite(ledPin, HIGH); // Liga o LED
        delay(interval);           // Aguarda um intervalo
        digitalWrite(ledPin, LOW); // Desliga o LED
        delay(interval);           // Aguarda outro intervalo
    }
}


void setup() {
    pinMode(ledPin, OUTPUT);
    pinMode(micPin, INPUT);
    Serial.begin(115200, SERIAL_8N1);
}

void loop(){
    if (Serial.available() ) {
       charRecebido = Serial.read();
       switch (charRecebido) {
         case 'l':
           ledState = 1;
           break;
         case 'd':
           ledState = 0;
           break;
         case 'i':
           iniciaColeta = 1;
           break;
         case 'p':
           iniciaColeta = 0;
           break;
        default: 
            break;
        
       }
    }
    if(iniciaColeta == 1){
        int valorSensor = analogRead(micPin);
        Serial.write(valorSensor & 0xFF); //byte mais significativo
        Serial.write((valorSensor >> 8)); //byte menos significativo
    }
    if(ledState == 1){
        alarm(4, loopDelay/10)
    }


  delay(loopDelay);
}
