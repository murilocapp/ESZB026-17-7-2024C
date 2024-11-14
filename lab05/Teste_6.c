// Ajustando o PWM por HARDWARE na Raspberry Pi

#include <stdio.h>
#include <wiringPi.h>

#define pino_PWM0 18                    // o PWM sera acionado na GPIO18

int main() {                            // este programa deve ser rodado com 'sudo'
   int dc, ciclos,frequencia;
   wiringPiSetupGpio();                 // usa a numeracao da GPIO
   pinMode(pino_PWM0, PWM_OUTPUT);      // configura a GPIO18 com o PWM por hardware

   // Ajustando a frequencia do PWM em 10kHz com 128 passos de duty cycle
   // frequencia PWM = 19,2 MHz / (divisor * range)
   // freq = 1000Hz
   pwmSetMode(PWM_MODE_MS);             // usando frequencia fixa
   pwmSetRange(128);                    // (range) passos do duty cycle (max=4096)
   pwmSetClock(150);                    // (divisor) fornece uma frequencia de 10kHz (max=4096)
   printf("Iniciando...\n");
   
   pwmWrite(pino_PWM0, 0);
   usleep(3000000);
   for(ciclos = 0; ciclos < 4; ciclos++){  // variando o duty cycle
      for(dc = 25; dc < 40; dc++){
         pwmWrite(pino_PWM0, dc);
         printf("dc = %d\n",dc);
         usleep(1000000);
      }
      pwmWrite(pino_PWM0, 0);
      usleep(3000000);
   }
   pwmWrite(pino_PWM0, 0);
   printf("Fim.\n");
   return 0;              
}
