// Autor: Joahannes B. D. da Costa <joahannes.costa@unifesp.br>
// Data: 23.04.2025

// I/O padrão
#include <stdio.h>

void funcao_recursiva(int contador) {
    printf("Chamada número: %d\n", contador);
    funcao_recursiva(contador + 1); 
}

int main() {
    funcao_recursiva(1);
    return 0;
}