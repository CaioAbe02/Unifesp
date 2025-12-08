/* ast.h */
#ifndef AST_H
#define AST_H

typedef enum {
    NodeK_Stmt,
    NodeK_Expr,
    NodeK_Decl
} NodeKind;

typedef enum {
    StmtK_If, StmtK_While, StmtK_Return, StmtK_Assign, StmtK_Comp
} StmtKind;

typedef enum {
    ExprK_Op, ExprK_Id, ExprK_Num, ExprK_Call
} ExprKind;

typedef enum {
    DeclK_Var, DeclK_Func, DeclK_Param
} DeclKind;

typedef struct treeNode {
    NodeKind nodekind;

    union {
        StmtKind stmt;
        ExprKind expr;
        DeclKind decl;
    } kind;

    struct treeNode *child[3];
    struct treeNode *sibling;

    int lineno;

    /* atributos */
    char *name;       /* para ID */
    int val;          /* para NUM */
    int op;           /* para operadores */
} TreeNode;

TreeNode *newDeclNode(DeclKind kind);
TreeNode *newStmtNode(StmtKind kind);
TreeNode *newExprNode(ExprKind kind);

TreeNode *addSibling(TreeNode *t1, TreeNode *t2);

void printTree(TreeNode *tree);

#endif
