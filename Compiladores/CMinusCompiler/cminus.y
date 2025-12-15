%{
#include "globals.h"
#include "ast.h"

extern int yylex(void);
extern char *yytext;
void yyerror(const char *s);

int func_lineno;
%}

%printer { fprintf (yyoutput, "'%d'", $$); } NUM

%union {
  TreeNode *tnode;
  int value;
  char *name;
}

%type <tnode> program declaration_list declaration var_declaration fun_declaration params param_list param compound_decl local_declarations statement_list statement expression_decl selection_decl iteration_decl return_decl expression var simple_expression sum_expression term factor activation args arg_list
%type <name> relational sum mult
%type <value> type_specifier

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
            root = $1;
        }

declaration_list  : declaration_list declaration {
                      $$ = addSibling($1, $2);
                  }
                  | declaration {
                      $$ = $1;
                  };

declaration : var_declaration {
                $$ = $1;
            }
            | fun_declaration {
                $$ = $1;
            };

var_declaration : type_specifier ID SEMI {
                    $$ = newDeclNode(DeclK_Var);
                    $$->name = $2;
                    $$->lineno = lineno;
                    $$->type = $1;
                  }
                | type_specifier ID LBRACKET NUM RBRACKET SEMI {
                    $$ = newDeclNode(DeclK_Var);
                    $$->name = $2;
                    $$->lineno = lineno;
                    $$->type = $1;
                  };

type_specifier  : INT { $$ = Integer; }
                | VOID { $$ = Void; };

fun_declaration : type_specifier ID {
                    func_lineno = lineno;
                  }
                  LPAREN params RPAREN compound_decl {
                    $$ = newDeclNode(DeclK_Func);
                    $$->lineno = func_lineno;
                    $$->name = $2;
                    $$->child[1] = $5;
                    $$->child[2] = $7;
                    $$->type = $1;
                    updateScope($$->child[1], $$->name);
                    updateScope($$->child[2], $$->name);
                  };

params  : param_list {
            $$ = $1;
        }
        | VOID {
            $$ = NULL;
        };

param_list: param_list COMMA param {
              $$ = addSibling($1, $3);
          }
          | param {
              $$ = $1;
          };

param: type_specifier ID {
         $$ = newDeclNode(DeclK_Param);
         $$->name = $2;
         $$->lineno = lineno;
         $$->type = $1;
       }
     | type_specifier ID LBRACKET RBRACKET {
         $$ = newDeclNode(DeclK_Param);
         $$->name = $2;
         $$->lineno = lineno;
         $$->type = $1;
       };

compound_decl : LBRACE local_declarations statement_list RBRACE {
                  $$ = newStmtNode(StmtK_Comp);
                  $$->child[0] = $2;
                  $$->child[1] = $3;
                };

local_declarations: local_declarations var_declaration {
                      $$ = addSibling($1, $2);
                  }
                  | /* empty */ {
                      $$ = NULL;
                  };

statement_list  : statement_list statement {
                    $$ = addSibling($1, $2);
                }
                | /* empty */ {
                    $$ = NULL;
                };

statement: expression_decl { $$ = $1; }
         | compound_decl { $$ = $1; }
         | selection_decl { $$ = $1; }
         | iteration_decl { $$ = $1; }
         | return_decl { $$ = $1; };

expression_decl : expression SEMI {
                    $$ = newStmtNode(StmtK_Expr);
                    $$->child[0] = $1;
                    $$->lineno = lineno;
                  }
                | SEMI {
                    $$ = NULL;
                  };

selection_decl: IF LPAREN expression RPAREN statement {
                  $$ = newStmtNode(StmtK_If);
                  $$->child[0] = $3;
                  $$->child[1] = $5;
                  $$->lineno = lineno;
              }
              | IF LPAREN expression RPAREN statement ELSE statement {
                  $$ = newStmtNode(StmtK_If);
                  $$->child[0] = $3;
                  $$->child[1] = $5;
                  $$->child[2] = $7;
                  $$->lineno = lineno;
              };

iteration_decl: WHILE LPAREN expression RPAREN statement {
                  $$ = newStmtNode(StmtK_While);
                  $$->child[0] = $3;
                  $$->child[1] = $5;
                  $$->lineno = lineno;
              };

return_decl: RETURN SEMI {
                $$ = newStmtNode(StmtK_Return);
                $$->lineno = lineno;
           }
           | RETURN expression SEMI {
                $$ = newStmtNode(StmtK_Return);
                $$->child[0] = $2;
                $$->lineno = lineno;
           };

expression: var ASSIGN expression {
              $$ = newStmtNode(StmtK_Assign);
              $$->name = $1->name;
              $$->child[0] = $1;
              $$->child[1] = $3;
              $$->lineno = lineno;
          }
          | simple_expression {
              $$ = $1;
          };

var: ID {
       $$ = newExprNode(ExprK_Id);
       $$->name = $1;
       $$->lineno = lineno;
   }
   | ID LBRACKET expression RBRACKET {
       $$ = newExprNode(ExprK_Id);
       $$->name = $1;
       $$->child[0] = $3;
       $$->lineno = lineno;
   };

simple_expression: sum_expression relational sum_expression {
                     $$ = newExprNode(ExprK_Op);
                     $$->child[0] = $1;
                     $$->child[1] = $3;
                     $$->op = $2;
                     $$->lineno = lineno;
                 }
                 | sum_expression {
                     $$ = $1;
                 };

relational: LESS { $$ = "<"; }
          | LESSEQUAL { $$ = "<="; }
          | GREATER { $$ = ">"; }
          | GREATEREQUAL { $$ = ">="; }
          | EQUAL { $$ = "=="; }
          | NOTEQUAL { $$ = "!="; };

sum_expression: sum_expression sum term {
                  $$ = newExprNode(ExprK_Op);
                  $$->child[0] = $1;
                  $$->child[1] = $3;
                  $$->op = $2;
                  $$->lineno = lineno;
              }
              | term {
                  $$ = $1;
              };

sum: PLUS { $$ = "+"; }
   | MINUS { $$ = "-"; };

term: term mult factor {
        $$ = newExprNode(ExprK_Op);
        $$->child[0] = $1;
        $$->child[1] = $3;
        $$->op = $2;
        $$->lineno = lineno;
    }
    | factor {
        $$ = $1;
    };

mult: TIMES { $$ = "*"; }
    | OVER { $$ = "/"; };

factor: LPAREN expression RPAREN {
          $$ = $2;
      }
      | var {
          $$ = $1;
      }
      | activation {
          $$ = $1;
      }
      | NUM {
          $$ = newExprNode(ExprK_Num);
          $$->val = $1;
          $$->lineno = lineno;
      };

activation: ID LPAREN args RPAREN {
              $$ = newExprNode(ExprK_Call);
              $$->name = $1;
              $$->child[0] = $3;
              $$->lineno = lineno;
          };

args: arg_list {
        $$ = $1;
    }
    | /* empty */ {
        $$ = NULL;
    };

arg_list: arg_list COMMA expression {
            $$ = addSibling($1, $3);
        }
        | expression {
            $$ = $1;
        };

%%

void yyerror(const char *s) {
  fprintf(stderr, "SYNTAX ERROR: %s LINE: %d\n", yytext, lineno);
}