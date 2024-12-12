const int ledPin = 2; //pino digital de saida do led
const int micPin = A0; //pino do microfone 
int ledState = 0; //inicia com led desligado
int iniciaColeta = 0; //variavel de estado da coleta
int freqAquisicao = 1; //em Hz
char charRecebido;

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
        
    }


  delay(freqAquisicao*1000);
}
