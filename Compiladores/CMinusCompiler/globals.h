#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "ast.h"
#include "cminus.tab.h"

#define MAXCHILDREN 3

extern int lineno;
extern FILE * listing;
extern TreeNode *root;