#include <stdio.h>
#include <ctype.h>
#include <stdbool.h>
#include <string.h>

char buffer[256];
int pos;

// Definição dos estados
// 1 = inicial, 2 = lendo identificador, 3 = aceitação, 4 = erro
int T[5][3] = {
  {0, 0, 0},  // índice 0 não usado
  {2, 4, 4},  // estado 1
  {2, 2, 3},  // estado 2
  {3, 3, 3},  // estado 3 (final)
  {4, 4, 4}   // estado 4 (erro)
};

// Avanço da entrada (se consome caractere ou não)
bool Avance[5][3] = {
  {false, false, false},
  {true,  false, false},  // estado 1
  {true,  true,  false},  // estado 2
  {false, false, false},  // estado 3
  {false, false, false}   // estado 4
};

// Aceitação
bool Aceita[5] = {false, false, false, true, false};

// Função para classificar caracteres
int classeChar(char ch) {
  if (isalpha((unsigned char)ch)) return 0;   // letra
  if (isdigit((unsigned char)ch)) return 1;   // dígito
  return 2;                                   // outro
}

int main() {
  FILE *entrada = fopen("sort.txt", "r");
  FILE *saida   = fopen("saida.txt", "w");

  if (!entrada) {
    printf("Erro ao abrir sort.txt\n");
    return 1;
  }

  char ch;
  while ((ch = fgetc(entrada)) != EOF) {
    int estado = 1;  // estado inicial

    if (isalpha((unsigned char)ch)) {
      pos = 0;
      buffer[pos++] = ch;

      // Inicia identificador
      estado = T[estado][classeChar(ch)];

      while (!Aceita[estado]) {
        int prox = fgetc(entrada);
        if (prox == EOF) {
          break;
        }

        int c = classeChar((char)prox);
        int novo_estado = T[estado][c];

        if (Avance[estado][c]) {
          buffer[pos++] = (char)prox;
          estado = novo_estado;
        } else {
          ungetc(prox, entrada); // devolve caractere não consumido
          estado = novo_estado;
        }
      }
      buffer[pos] = '\0';  // finaliza string do identificador
      if (strcmp(buffer, "int") == 0 ||
        strcmp(buffer, "void") == 0 ||
        strcmp(buffer, "return") == 0 ||
        strcmp(buffer, "while") == 0 ||
        strcmp(buffer, "if") == 0 ||
        strcmp(buffer, "else") == 0 ||
        strcmp(buffer, "for") == 0) {
        fprintf(saida, "%s", buffer); // mantém palavra reservada
      } else {
        fprintf(saida, "ID"); // substitui por token
      }
    } else {
      // Qualquer outro caractere é copiado
      fputc(ch, saida);
    }
  }

  fclose(entrada);
  fclose(saida);

  printf("Concluído\n");
  return 0;
}
