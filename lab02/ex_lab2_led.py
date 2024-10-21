import time
import os

# Definindo os GPIOs dos LEDs
RED_GPIO = 16
GREEN_GPIO = 20
YELLOW_GPIO = 21

# Função para habilitar GPIO
def setup_gpio(gpio):
    os.system(f"echo {gpio} > /sys/class/gpio/export")
    time.sleep(1)
    os.system(f"echo out > /sys/class/gpio/gpio{gpio}/direction")

# Função para desligar GPIO
def cleanup_gpio(gpio):
    os.system(f"echo {gpio} > /sys/class/gpio/unexport")

# Habilitando os LEDs
setup_gpio(RED_GPIO)
setup_gpio(GREEN_GPIO)
setup_gpio(YELLOW_GPIO)

# Sequência de LEDs
for _ in range(5):
    os.system(f"echo 1 > /sys/class/gpio/gpio{RED_GPIO}/value")
    time.sleep(2)
    os.system(f"echo 0 > /sys/class/gpio/gpio{RED_GPIO}/value")
    
    os.system(f"echo 1 > /sys/class/gpio/gpio{GREEN_GPIO}/value")
    time.sleep(1)
    os.system(f"echo 0 > /sys/class/gpio/gpio{GREEN_GPIO}/value")
    
    os.system(f"echo 1 > /sys/class/gpio/gpio{YELLOW_GPIO}/value")
    time.sleep(1)
    os.system(f"echo 0 > /sys/class/gpio/gpio{YELLOW_GPIO}/value")

# Desabilitando os LEDs
cleanup_gpio(RED_GPIO)
cleanup_gpio(GREEN_GPIO)
cleanup_gpio(YELLOW_GPIO)
