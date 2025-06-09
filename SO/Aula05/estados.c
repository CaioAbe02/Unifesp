// Autor: Joahannes B. D. da Costa <joahannes.costa@unifesp.br>
// Data: 23.04.2025

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

typedef enum { BLOQUEADO, PRONTO, EM_EXECUCAO } Estado;

// Função para exibir o estado atual
void exibir_estado(Estado estado) {
    switch (estado) {
        case BLOQUEADO:
            printf("\nEstado atual do processo: [Bloqueado]");
            break;
        case PRONTO:
            printf("\nEstado atual do processo: [Pronto]");
            break;
        case EM_EXECUCAO:
            printf("\nEstado atual do processo: [Em execução]");
            break;
    }
}

// Função principal para simular transições de estados
int main() {

    printf("---------------------------\n");
    printf("|  SO - UNIFESP - 1s2025  |\n");
    printf("---------------------------\n");

    Estado estado = PRONTO; // Estado inicial do processo
    int transicao;

    while (1) {
        exibir_estado(estado);
        
        printf("\nEscolha a transição de estado (1 a 4, ou 0 para sair): ");
        scanf("%d", &transicao);
        
        switch (transicao) {
            case 1:
                if (estado == EM_EXECUCAO) {
                    estado = BLOQUEADO;
                    printf("Transição 1: Em execução -> Bloqueado\n");
                } else {
                    printf("Transição inválida!\n");
                }
                break;
            case 2:
                if (estado == EM_EXECUCAO) {
                    estado = PRONTO;
                    printf("Transição 2: Em execução -> Pronto\n");
                } else {
                    printf("Transição inválida!\n");
                }
                break;
            case 3:
                if (estado == PRONTO) {
                    estado = EM_EXECUCAO;
                    printf("Transição 3: Pronto -> Em execução\n");
                } else {
                    printf("Transição inválida!\n");
                }
                break;
            case 4:
                if (estado == BLOQUEADO) {
                    estado = PRONTO;
                    printf("Transição 4: Bloqueado -> Pronto\n");
                } else {
                    printf("Transição inválida!\n");
                }
                break;
            case 0:
                printf("Saindo...\n");
                exit(0);
            default:
                printf("Transição inválida!\n");
        }
        sleep(1);
    }

    return 0;
}
