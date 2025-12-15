run:
	flex cminus.l
	-bison -d cminus.y
	gcc ast.c analyze.c symtab.c cminus.tab.c lex.yy.c main.c -o cminus.exe