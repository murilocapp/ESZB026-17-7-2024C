#include <stdio.h>
#include <wiringPi.h>

#define pino_PWMO 18

int main() {
	int dc,ciclos;
	wiringPiSetupGpio();
	pinMode(pino_PWMO, PWM_OUTPUT);
	
	double c4 = 261.6;
	
	
	// 260 = 19200000 / (div * 128) => 
	pwmSetMode(c4);
	pwmSetRange(128);
	pwmSetClock(577);
	
	// seq => c4, pausa, c4, pausa, c4, pausa, c4, pausa
	for(ciclos = 0; ciclos < 4; ciclos ++){
		//ligado
		pwmWrite(pino_PWMO, 64);
		//desligado
		usleep(10000);
	}
	

}
