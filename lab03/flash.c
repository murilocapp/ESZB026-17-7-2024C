#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>  // for usleep()
#include <fcntl.h>   // for open()
#include <string.h>  // for strlen()

// Função para escrever um valor em um arquivo do sistema
void write_to_file(const char* path, const char* value) {
    int fd = open(path, O_WRONLY);
    if (fd == -1) {
        perror("Failed to open file");
        exit(1);
    }

    if (write(fd, value, strlen(value)) == -1) {
        perror("Failed to write to file");
        exit(1);
    }

    close(fd);
}

int main() {
    // Exportar o pino GPIO 23
    write_to_file("/sys/class/gpio/export", "23");
    usleep(500000);  // esperar 0.5 segundos

    // Definir a direção do pino como saída
    write_to_file("/sys/class/gpio/gpio23/direction", "out");

    // Alternar o valor do pino 20.000 vezes
    for (int counter = 0; counter < 20000; counter++) {
        write_to_file("/sys/class/gpio/gpio23/value", "1");
        write_to_file("/sys/class/gpio/gpio23/value", "0");
    }

    // Desexportar o pino GPIO 23
    write_to_file("/sys/class/gpio/unexport", "23");

    return 0;
}
