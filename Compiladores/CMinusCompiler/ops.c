#include "globals.h"
#include "symtab.h"
#include "analyze.h"
#include "ast.h"
#include <string.h>

static int location = 0;

/* Função auxiliar para percorrer a árvore (pre-order para buildSymtab) */
static void traverse(TreeNode *t, void (*preProc)(TreeNode *), void (*postProc)(TreeNode *)) {
    if (t != NULL) {
        preProc(t);
        {
            int i;
            for (i = 0; i < 3; i++)
                traverse(t->child[i], preProc, postProc);
        }
        postProc(t);
        traverse(t->sibling, preProc, postProc);
    }
}

static void nullProc(TreeNode *t) { 
    if (t == NULL) return; 
    else return; 
}

/* --- Build Symbol Table --- */

static void insertNode(TreeNode *t) {
    switch (t->nodekind) {
        case NodeK_Stmt:
            switch (t->kind.stmt) {
                case StmtK_Comp:
                    // Entra em um novo escopo para blocos compostos
                    st_enter_scope();
                    break;
                default:
                    break;
            }
            break;
        case NodeK_Expr:
            switch (t->kind.expr) {
                case ExprK_Id:
                case ExprK_Call:
                    // Verifica se o identificador foi declarado
                    if (st_lookup(t->name) == -1) {
                        /* Erro: não declarado */
                        printf("Erro Semantico: Variavel/Funcao '%s' nao declarada na linha %d\n", 
                               t->name, t->lineno);
                    }
                    break;
                default:
                    break;
            }
            break;
        case NodeK_Decl:
            switch (t->kind.decl) {
                case DeclK_Func:
                    // Verifica se função já foi declarada globalmente
                    if (st_lookup(t->name) != -1) {
                        printf("Erro Semantico: Funcao '%s' ja declarada na linha %d\n", 
                               t->name, t->lineno);
                    } else {
                        // Insere função no escopo global
                        st_insert(t->name, t->lineno, location++);
                    }
                    break;
                // No arquivo analyze.c, na seção DeclK_Var e DeclK_Param:
                case DeclK_Var:
                    if (t->name != NULL && strcmp(t->name, "int") != 0 && strcmp(t->name, "void") != 0) {
                        // Verifica se já existe no escopo atual
                        if (st_lookup_current_scope(t->name) != -1) {
                            printf("Erro Semantico: Variavel '%s' ja declarada neste escopo (linha %d)\n", 
                                  t->name, t->lineno);
                        } else {
                            // Insere no escopo atual
                            st_insert(t->name, t->lineno, 0);
                        }
                    }
                    break;
                case DeclK_Param:
                    if (t->name != NULL) {
                        // Parâmetro de função - verifica se já existe
                        if (st_lookup_current_scope(t->name) != -1) {
                            printf("Erro Semantico: Parametro '%s' ja declarado (linha %d)\n", 
                                  t->name, t->lineno);
                        } else {
                            st_insert(t->name, t->lineno, 0);
                        }
                    }
                    break;
            }
            break;
    }
}

static void afterInsertNode(TreeNode *t) {
    if (t->nodekind == NodeK_Stmt && t->kind.stmt == StmtK_Comp) {
        // Sai do escopo do bloco composto
        st_exit_scope();
    }
}

void buildSymtab(TreeNode *syntaxTree) {
    /* Adiciona funções predefinidas input e output se necessário */
    st_insert("input", 0, location++);
    st_insert("output", 0, location++);
    
    traverse(syntaxTree, insertNode, afterInsertNode);
    
    if (st_lookup("main") == -1) {
        printf("Erro Semantico: Funcao 'main' nao encontrada.\n");
    }
    
    printf("Tabela de simbolos construida com sucesso.\n");
}

/* --- Type Checking --- */

static void checkNode(TreeNode *t) {
    switch (t->nodekind) {
        case NodeK_Expr:
            switch (t->kind.expr) {
                case ExprK_Op:
                    // Verifica se ambos os operandos são inteiros
                    if (t->child[0] && t->child[1] && 
                        (t->child[0]->type != Integer || t->child[1]->type != Integer)) {
                        printf("Erro de Tipo: Operacao aritmetica aplicada a nao-inteiros na linha %d\n", 
                               t->lineno);
                    }
                    // Define o tipo do resultado
                    if (t->op && 
                        (!strcmp(t->op, "==") || !strcmp(t->op, "!=") ||
                         !strcmp(t->op, "<") || !strcmp(t->op, ">") ||
                         !strcmp(t->op, "<=") || !strcmp(t->op, ">="))) {
                        t->type = Boolean;
                    } else {
                        t->type = Integer;
                    }
                    break;
                case ExprK_Num:
                    t->type = Integer;
                    break;
                case ExprK_Id:
                case ExprK_Call:
                    // Por simplificação, assume que identificadores e chamadas retornam inteiros
                    t->type = Integer;
                    break;
            }
            break;
        case NodeK_Stmt:
            switch (t->kind.stmt) {
                case StmtK_If:
                case StmtK_While:
                    // Verifica se a expressão condicional é booleana ou inteira
                    if (t->child[0] && t->child[0]->type != Integer && t->child[0]->type != Boolean) {
                        printf("Erro de Tipo: Teste nao booleano/inteiro na linha %d\n", t->lineno);
                    }
                    break;
                case StmtK_Assign:
                    // Verifica compatibilidade de tipos na atribuição
                    if (t->child[0] && t->child[1] && 
                        t->child[0]->type != t->child[1]->type) {
                        printf("Erro de Tipo: Atribuicao invalida na linha %d\n", t->lineno);
                    }
                    break;
                default:
                    break;
            }
            break;
        default:
            break;
    }
}

void typeCheck(TreeNode *syntaxTree) {
    // Primeiro inicializa os tipos na árvore
    traverse(syntaxTree, nullProc, checkNode);
}