#include <stdio.h>
#include <stdlib.h>

int main() {
    // 1000
    int tamanho = 1000;
    // 2000
    // int tamanho = 2000;

    // alocacao estatica
    int matriz[tamanho][tamanho];

    int l = 0;

    // percorrer a matriz
    for (int i = 0; i < tamanho; i++) {
        for (int j = 0; j < tamanho; j++) {
            l = matriz[i][j];
        }
    }

    printf("Programa C\n");

    return 0;
}
