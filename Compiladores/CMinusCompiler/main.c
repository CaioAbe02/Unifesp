#include "globals.h"
#include "analyze.h"
#include "symtab.h"
#define YYDEBUG 1

int lineno = 1;
TreeNode *root;
FILE * listing;

extern FILE *yyin;
extern int yyparse(void);
extern char *yytext;
// extern int yydebug;

int main(int argc, char **argv) {
  // yydebug = 1;
  if (argc == 2) {
        yyin = fopen(argv[1], "r");
        if (!yyin) { perror("fopen"); return 1; }
    } else {
        yyin = stdin;
    }

    root = NULL;

    if (yyparse() == 0) {
      listing = stdout;

      printTree(root);
      printf("\n");

      buildSymtab(root);

      typeCheck(root);

      // printf("Building\n");
      // buildSymtab(root);

      // printf("Checking\n");
      // typeCheck(root);

      // printf("Tabela\n");
      // printSymTab(stdout);
    }
    return 0;
}
