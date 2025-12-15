#include "globals.h"
#include "symtab.h"
#include "analyze.h"

static int location = 0;

static void typeError(TreeNode * t, char * message)
{ fprintf(listing,"SEMANTIC ERROR: %s %s LINE: %d\n", t->name, message, t->lineno);
}

static void traverse( TreeNode * t,
                      void (* preProc) (TreeNode *),
                      void (* postProc) (TreeNode *) )
{ if (t != NULL)
  { preProc(t);
    { int i;
      for (i=0; i < MAXCHILDREN; i++)
        traverse(t->child[i],preProc,postProc);
    }
    postProc(t);
    traverse(t->sibling,preProc,postProc);
  }
}

static void nullProc(TreeNode * t)
{ if (t==NULL) return;
  else return;
}

static void insertNode( TreeNode * t)
{ switch (t->nodekind)
  { case NodeK_Decl:
      switch (t->kind.decl)
      { case DeclK_Var:
        case DeclK_Param:
          if (st_lookup(t->name, t->scope) == -1)
            st_insert(t->name,t->lineno,location++,t->scope,t->type);
          else
            typeError(t, "already declared");
          break;
        case DeclK_Func:
          if (st_lookup(t->name, "global") == -1)
            st_insert(t->name,t->lineno,location++,t->scope,t->type);
          else
            typeError(t, "already declared");
          break;
        default:
          break;
      }
      break;

    case NodeK_Expr:
      switch (t->kind.expr)
      { case ExprK_Id:
          if (st_lookup(t->name, t->scope) == -1) {
              if (st_lookup(t->name, "global") == -1) {
                  typeError(t, "not declared");
              } else {
                  st_insert(t->name, t->lineno, 0, "global", t->type);
              }
          } else {
              st_insert(t->name, t->lineno, 0, t->scope, t->type);
          }
          break;

        case ExprK_Call:
          if (st_lookup(t->name, "global") == -1)
            typeError(t, "not declared");
          else
            st_insert(t->name, t->lineno, 0, "global", t->type);
          break;
        default:
          break;
      }
      break;

    case NodeK_Stmt:
      switch (t->kind.stmt)
      { case StmtK_Assign:
          if (st_lookup(t->name, t->scope) == -1) {
              if (st_lookup(t->name, "global") == -1) {
                  typeError(t, "not declared");
              } else {
                  st_insert(t->name, t->lineno, 0, "global", Integer);
              }
          } else {
              st_insert(t->name, t->lineno, 0, t->scope, Integer);
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

void buildSymtab(TreeNode * syntaxTree)
{
  st_insert("input", 0, location++, "global", Integer);
  st_insert("output", 0, location++, "global", Void);

  traverse(syntaxTree,insertNode,nullProc);

  if (st_lookup("main", "global") == -1) {
      fprintf(listing, "SEMANTIC ERROR: main function not declared\n");
  }

  printSymTab(listing);
}

static void checkNode(TreeNode * t)
{ switch (t->nodekind)
  { case NodeK_Decl:
      switch (t->kind.decl)
      { case DeclK_Var:
        case DeclK_Param:
          if (t->type == Void)
            typeError(t, "declared with invalid type");
          break;
        case DeclK_Func:
          break;
      }
      break;
    case NodeK_Expr:
      switch (t->kind.stmt)
      { case StmtK_Assign:
        typeError(t->child[0], "assigned with invalid type");
          if (t->child[1])
            if (t->child[1]->type = Void)
              typeError(t->child[0], "assigned with invalid type");
          break;
      }
    default:
      break;
  }
}

void typeCheck(TreeNode * syntaxTree)
{ traverse(syntaxTree,nullProc,checkNode);
}
