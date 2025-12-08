%option noyywrap

%{
#include <stdlib.h>
#include <stdio.h>

#include "globals.h"
%}

DIGIT       [0-9]
NUMBER      {DIGIT}+
LETTER      [a-zA-Z]
IDENTIFIER  {LETTER}+
NEWLINE     \n
WHITESPACE  [ \t]+

%%
"/*"          { char c;
                do {
                  c = input();
                  if (c == EOF) break;
                  if (c == '\n') lineno++;
                  if (c == '*') {
                    if(input() == '/') {
                      break;
                    }
                  }
                } while (1);
              }
"else"        {return ELSE;}
"if"          {return IF;}
"int"         {return INT;}
"return"      {return RETURN;}
"void"        {return VOID;}
"while"       {return WHILE;}
"+"           {return PLUS;}
"-"           {return MINUS;}
"*"           {return TIMES;}
"/"           {return OVER;}
"<"           {return LESS;}
"<="          {return LESSEQUAL;}
">"           {return GREATER;}
">="          {return GREATEREQUAL;}
"=="          {return EQUAL;}
"!="          {return NOTEQUAL;}
"="           {return ASSIGN;}
";"           {return SEMI;}
","           {return COMMA;}
"("           {return LPAREN;}
")"           {return RPAREN;}
"["           {return LBRACKET;}
"]"           {return RBRACKET;}
"{"           {return LBRACE;}
"}"           {return RBRACE;}
{IDENTIFIER}  {return ID;}
{NUMBER}      {return NUM;}
{NEWLINE}     {lineno++;}
{WHITESPACE}  { }
.             {return ERROR;}
<<EOF>>       {return END;}
%%
