%{
#include "globals.h"
#include "ast.h"

TreeNode *root;
extern int yylex(void);
%}

%union {
    TreeNode *tnode;   /* nós da AST */
    int value;         /* para números */
    char *name;        /* para IDs */
}

%type <tnode> program declaration_list declaration var_declaration type_specifier

%token <value> NUM
%token <name> ID
%token ELSE IF INT RETURN VOID WHILE
%token PLUS MINUS TIMES OVER ASSIGN
%token LESS LESSEQUAL GREATER GREATEREQUAL EQUAL NOTEQUAL
%token SEMI COMMA LPAREN RPAREN LBRACKET RBRACKET LBRACE RBRACE
%token ERROR END

%start program
%%

program : declaration_list {
            // root = $1;
          };

declaration_list  : declaration_list declaration {
                      $$ = addSibling($1, $2);
                    }
                  | declaration {
                      // // $$ = $1;
                    };

declaration : var_declaration {
                // $$ = $1;
              }
            | fun_declaration {
                // $$ = $1;
              };

var_declaration : type_specifier ID SEMI {
                    // $$ = newDeclNode(DeclK_Var);
                    // $$ -> name = strdup($2);
                  }
                | type_specifier ID LBRACKET NUM RBRACKET SEMI;

type_specifier  : INT {
                    // $$ = newD
                  }
                | VOID;

fun_declaration: type_specifier ID LPAREN params RPAREN compound_decl;

params: param_list | VOID;

param_list: param_list COMMA param | param;

param: type_specifier ID | type_specifier ID LBRACKET RBRACKET;

compound_decl: LBRACE local_declarations statement_list RBRACE;

local_declarations: local_declarations var_declaration | /* empty */;

statement_list: statement_list statement | /* empty */;

statement: expression_decl | compound_decl | selection_decl | iteration_decl | return_decl;

expression_decl: expression SEMI | SEMI;

selection_decl: IF LPAREN expression RPAREN statement | IF LPAREN expression RPAREN statement ELSE statement;

iteration_decl: WHILE LPAREN expression RPAREN statement;

return_decl: RETURN SEMI | RETURN expression SEMI;

expression: var ASSIGN expression | simple_expression;

var: ID | ID LBRACKET expression RBRACKET;

simple_expression: sum_expression relational sum_expression | sum_expression;

relational: LESS | LESSEQUAL | GREATER | GREATEREQUAL | EQUAL | NOTEQUAL;

sum_expression: sum_expression sum term | term;

sum: PLUS | MINUS;

term: term mult factor | factor;

mult: TIMES | OVER;

factor: LPAREN expression RPAREN | var | activation | NUM;

activation: ID LPAREN args RPAREN;

args: arg_list | /* empty */;

arg_list: arg_list COMMA expression | expression;

%%