/* ast.h */
#ifndef AST_H
#define AST_H

typedef enum {
    NodeK_Stmt,
    NodeK_Expr,
    NodeK_Decl,
} NodeKind;

typedef enum {
    StmtK_If, StmtK_While, StmtK_Return, StmtK_Assign, StmtK_Comp, StmtK_Expr
} StmtKind;

typedef enum {
    ExprK_Op, ExprK_Id, ExprK_Num, ExprK_Call, ExpreK_Type
} ExprKind;

typedef enum {
    DeclK_Var, DeclK_Func, DeclK_Param
} DeclKind;

typedef enum {Void, Integer} ExpType;

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
    char *name;
    int val;
    char *op;
    char *scope;
    ExpType type;
} TreeNode;

TreeNode *newDeclNode(DeclKind kind);
TreeNode *newStmtNode(StmtKind kind);
TreeNode *newExprNode(ExprKind kind);

TreeNode *addSibling(TreeNode *t1, TreeNode *t2);

void updateScope(TreeNode *t, char *scope);

void printTree(TreeNode *tree);

#endif
