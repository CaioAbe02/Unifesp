#include <stdio.h>
#include "globals.h"
#include "tokens.h"
#include "ast.h"

int lineno = 1;

extern FILE *yyin;
extern int yyparse(void);
extern char *yytext;

TreeNode *root;

int main(int argc, char **argv) {
  if (argc == 2) {
        yyin = fopen(argv[1], "r");
        if (!yyin) { perror("fopen"); return 1; }
    } else {
        yyin = stdin;
    }

    if (yyparse() == 0) {
      printTree(root);
    }

    else {
      printf("Erro!");
    }

    // int tok;
    // while ((tok = yylex()) != END) {
    //     switch(tok) {
    //       case NUM: printf("NUM "); break;
    //       case ID:  printf("ID ");  break;
    //       case ELSE:  printf("ELSE ");  break;
    //       case IF:  printf("IF ");  break;
    //       case INT:  printf("INT ");  break;
    //       case RETURN:  printf("RETURN ");  break;
    //       case WHILE:  printf("WHILE ");  break;
    //       case LESS:  printf("< ");  break;
    //       case LESSEQUAL:  printf("<= ");  break;
    //       case GREATER:  printf("> ");  break;
    //       case GREATEREQUAL:  printf(">= ");  break;
    //       case EQUAL:  printf("== ");  break;
    //       case NOTEQUAL:  printf("!= ");  break;
    //       case PLUS: printf("+ ");   break;
    //       case MINUS: printf("- ");   break;
    //       case TIMES: printf("* ");   break;
    //       case OVER: printf("/ ");   break;
    //       case ASSIGN: printf("= ");  break;
    //       case SEMI: printf(";\n"); break;
    //       case COMMA:  printf(", ");  break;
    //       case LPAREN: printf("( ");   break;
    //       case RPAREN: printf(") ");   break;
    //       case LBRACKET:  printf("[ ");  break;
    //       case RBRACKET:  printf("] ");  break;
    //       case LBRACE:  printf("{\n");  break;
    //       case RBRACE:  printf("}\n");  break;
    //       case ERROR: printf("ERROR "); break;
    //     }
    // }
    return 0;
}
