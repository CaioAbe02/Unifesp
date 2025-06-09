// Autor: Joahannes B. D. da Costa <joahannes.costa@unifesp.br>
// Data: 23.04.2025

// Fornece função que aloca memória na pilha da função chamadora
#include <alloca.h>
// I/O padrão
#include <stdio.h>
#include <time.h>

void funcao_recursiva(int bytes) {
    printf("Alocados %d bytes\n", bytes);
    bytes += 128;
    *((volatile char *) alloca(128)) = 0;
    // printf("[%d] bytes alocados - Chamada número [%d]\n", bytes, contador);
    // sleep(1);
    funcao_recursiva(bytes);
}

int main() {
    funcao_recursiva(0);
    return 0;
}
