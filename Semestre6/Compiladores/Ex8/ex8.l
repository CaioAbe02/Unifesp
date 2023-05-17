digit [0-9]
letter [a-zA-Z]
whitespace [ \t\r]+

%{
int lineno = 1;
%}
%%
{whitespace}    { }

"/*"		    { char c;
				  while(1){
					c = input();
					if(c==EOF) break;
					if(c=='\n') lineno++;
					if(c=='*'){
						c = input();
						if(c=='/') break;
						}
					}
				}

"if"            {return IF;}
%%
int main(int argc, char *argv[])
{
    FILE *f_in;

    if (argc == 2) {
        if(f_in = fopen(argv[1],"r")) yyin = f_in;
        else perror(argv[0]);
    }
    else yyin = stdin;

    yylex();
    return(0);
}