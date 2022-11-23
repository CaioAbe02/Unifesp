// C program to implement
// the above approach
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define true 1
#define false 0

#define letra 0
#define digito 1
#define outro 2

// Driver code
int main()
{
	FILE* ptr;
	char ch;

    int estado = 0;
    int novoestado = 0;
    int erro = false;
    int T[2][3] = {{1}, {2, 2, 3}};
    int Avance[2][3] = {{true}, {true, true, false}};
    int Aceita[3] = {false, false, true};

	// Opening file in reading mode
	ptr = fopen("ex6.txt", "r");

	if (NULL == ptr) {
		printf("file can't be opened \n");
	}

    if ((ch = fgetc(ptr)) == EOF) {
        erro = true;
    }

    while (!Aceita[estado] && !erro && ch != EOF) {
        if (isalpha(ch)) {
            novoestado = T[estado][letra];
            if (Avance[estado][letra]) {
                ch = fgetc(ptr);
            }
        }
        else if (isdigit(ch)) {
            novoestado = T[estado][digito];
            if (Avance[estado][digito]) {
                ch = fgetc(ptr);
            }
        }
        estado = novoestado;
    }

    if (Aceita[estado]) {
        printf("Passou!\n");
    }

	fclose(ptr);
	return 0;
}   
