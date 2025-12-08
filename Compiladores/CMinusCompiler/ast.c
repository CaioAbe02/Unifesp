/* ast.c */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ast.h"

static int indentno = 0;

/* controlando indentação */
#define INDENT indentno+=2
#define UNINDENT indentno-=2

static void printSpaces(void) {
    for (int i = 0; i < indentno; i++)
        printf(" ");
}

/* criação de nós */
TreeNode *newDeclNode(DeclKind kind) {
    TreeNode *t = (TreeNode *)malloc(sizeof(TreeNode));
    for (int i = 0; i < 3; i++) t->child[i] = NULL;
    t->sibling = NULL;
    t->nodekind = NodeK_Decl;
    t->kind.decl = kind;
    t->lineno = 0;
    t->name = NULL;
    t->val = 0;
    t->op  = 0;
    return t;
}

TreeNode *newStmtNode(StmtKind kind) {
    TreeNode *t = (TreeNode *)malloc(sizeof(TreeNode));
    for (int i = 0; i < 3; i++) t->child[i] = NULL;
    t->sibling = NULL;
    t->nodekind = NodeK_Stmt;
    t->kind.stmt = kind;
    t->lineno = 0;
    t->name = NULL;
    t->val = 0;
    t->op  = 0;
    return t;
}

TreeNode *newExprNode(ExprKind kind) {
    TreeNode *t = (TreeNode *)malloc(sizeof(TreeNode));
    for (int i = 0; i < 3; i++) t->child[i] = NULL;
    t->sibling = NULL;
    t->nodekind = NodeK_Expr;
    t->kind.expr = kind;
    t->lineno = 0;
    t->name = NULL;
    t->val = 0;
    t->op  = 0;
    return t;
}

/* adiciona irmãos */
TreeNode *addSibling(TreeNode *t1, TreeNode *t2) {
    if (t1 == NULL) return t2;
    TreeNode *temp = t1;
    while (temp->sibling != NULL)
        temp = temp->sibling;
    temp->sibling = t2;
    return t1;
}

/* imprime a árvore */
void printTree(TreeNode *tree) {
    if (tree == NULL) return;

    INDENT;
    while (tree != NULL) {
        printSpaces();

        switch (tree->nodekind) {
            case NodeK_Decl:
                switch (tree->kind.decl) {
                    case DeclK_Var: printf("Decl: Var %s\n", tree->name); break;
                    case DeclK_Param: printf("Decl: Param %s\n", tree->name); break;
                    case DeclK_Func: printf("Decl: Func %s\n", tree->name); break;
                }
                break;

            case NodeK_Stmt:
                switch (tree->kind.stmt) {
                    case StmtK_Assign: printf("Stmt: Assign to %s\n", tree->name); break;
                    case StmtK_If:     printf("Stmt: If\n"); break;
                    case StmtK_While:  printf("Stmt: While\n"); break;
                    case StmtK_Return: printf("Stmt: Return\n"); break;
                    case StmtK_Comp:   printf("Stmt: Compound\n"); break;
                }
                break;

            case NodeK_Expr:
                switch (tree->kind.expr) {
                    case ExprK_Id:   printf("Expr: Id %s\n", tree->name); break;
                    case ExprK_Num:  printf("Expr: Const %d\n", tree->val); break;
                    case ExprK_Op:   printf("Expr: Op %d\n", tree->op); break;
                    case ExprK_Call: printf("Expr: Call %s\n", tree->name); break;
                }
                break;
        }

        for (int i = 0; i < 3; i++)
            printTree(tree->child[i]);

        tree = tree->sibling;
    }
    UNINDENT;
}
