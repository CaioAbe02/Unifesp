// Autor: Joahannes B. D. da Costa <joahannes.costa@unifesp.br>
// Data: 23.04.2025

// Fornece função que aloca memória na pilha da função chamadora
#include <alloca.h>
// I/O padrão
#include <stdio.h>
#include <time.h>

int main() {
    int n = 0;
    for (;;) {
        printf("Alocados %d bytes\n", n);
        fflush(stdout);
        n += 128;
        *((volatile char *) alloca(128)) = 0;
    }
    return 0;
}
