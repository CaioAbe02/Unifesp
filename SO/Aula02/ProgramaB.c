#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    int **matriz;
    int l = 0;

    // Alocar dinamicamente uma matriz 20000x20000
    int tamanho = 20000;
    matriz = (int **)malloc(tamanho * sizeof(int *));
    for (int i = 0; i < tamanho; i++) {
        matriz[i] = (int *)malloc(tamanho * sizeof(int));
    }

    if (matriz == NULL) {
        printf("Erro ao alocar memória!\n");
        return 1;
    }

    clock_t inicio = clock();

    // Percorrer a matriz
    for (int i = 0; i < tamanho; i++) {
        for (int j = 0; j < tamanho; j++) {
            l = matriz[j][i];
        }
    }

    clock_t fim = clock();

    // Liberar a memória alocada
    for (int i = 0; i < tamanho; i++) {
        free(matriz[i]);
    }
    free(matriz);

    double tempo_gasto = (double)(fim - inicio) / CLOCKS_PER_SEC;
    printf("Programa B: %f segundos.\n", tempo_gasto);

    return 0;
}
