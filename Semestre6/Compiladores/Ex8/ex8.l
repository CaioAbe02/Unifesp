DIGIT [0-9]
LETTER[a-zA-Z]
WHITESPACE[ ]
QUEBRA [\n]
%%
"{"({WHITESPACE}*|{DIGIT}*|{LETTER}*)"}" printf("Comment Start");
%%
int main(int argc, char *argv[])
{
FILE *f_in;

if (argc == 2)
{
if(f_in = fopen(argv[1],"r")) yyin = f_in;
else perror(argv[0]);
}
else yyin = stdin;

yylex();
return(0);
}