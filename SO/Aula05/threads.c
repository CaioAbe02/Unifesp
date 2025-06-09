#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

#define NUMBER_OF_THREADS 5

void *print_hello_world(void *tid) {
    /* Esta função imprime o identificador do thread e sai. */
    printf("Thread [%d] iniciada!\n", (int) tid);
    sleep(2);
    printf("Thread [%d] encerrada!\n", (int) tid);
    pthread_exit(NULL);
}

int main(int argc, char *argv[]) {
    /* O programa principal cria 5 threads e sai. */
    pthread_t threads[NUMBER_OF_THREADS];
    int status, i;

    for (i = 0; i < NUMBER_OF_THREADS; i++) {
        printf("Método Main. Criando thread %d\n", i);
        status = pthread_create(&threads[i], NULL, print_hello_world, (void *) i);
        printf("Status de criação da thread %d: %d\n\n", i, status);
        // pthread_join(i, NULL);
        if (status != 0) {
            printf("Oops. pthread_create retornou o código de erro %d\n", status);
            return -1;
        }
    }

    // // Espera todos os threads terminarem
    for (i = 0; i < NUMBER_OF_THREADS; i++) {
        status = pthread_join(threads[i], NULL);
        if (status != 0) {
            printf("Erro ao esperar o término do thread %d. Código de erro: %d\n", i, status);
            exit(-1);
        }
    }

    printf("Todos os threads terminaram. Finalizando o programa principal.\n");
    return 0;
}
