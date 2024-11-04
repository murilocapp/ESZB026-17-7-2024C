#!/usr/bin/python

import time
import RPi.GPIO as GPIO
import serial


pino_PWM = 23  
frequencia = 100  
porta_serial = '/dev/ttyACM0'  
baud_rate = 115200  

# Configuração do pino GPIO e do PWM
GPIO.setmode(GPIO.BCM)
GPIO.setup(pino_PWM, GPIO.OUT)
pwm = GPIO.PWM(pino_PWM, frequencia)
pwm.start(0)  # Inicia o PWM com duty cycle 0%

# Configuração da comunicação serial
arduino = serial.Serial(porta_serial, baud_rate, timeout=1)
time.sleep(2)  

try:
    while True:
        if arduino.in_waiting > 0:  
            valor_pot = int(arduino.readline().decode().strip())
            brilho = (valor_pot / 1023) * 100
            pwm.ChangeDutyCycle(brilho)
            
        time.sleep(0.1) 

except KeyboardInterrupt:
    pass


pwm.stop()
GPIO.cleanup()
arduino.close()
