#include "ast.h"

void st_insert( char * name, int lineno, int loc, char * scope, ExpType type );

int st_lookup ( char * name, char * scope );

void printSymTab(FILE * listing);
