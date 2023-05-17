# Makefile for C-Minus compiler
# @trilliwon

CC = gcc
BISON = bison
LEX = flex

BIN = compiler

OBJS = tiny.tab.o lex.yy.o main.o util.o symtab.o analyze.o

$(BIN): $(OBJS)
	$(CC) $(OBJS) -o $(BIN)

main.o: main.c globals.h util.h scan.h analyze.h
	$(CC) -c main.c

util.o: util.c util.h globals.h
	$(CC) -c util.c

symtab.o: symtab.c symtab.h
	$(CC) -c symtab.c

analyze.o: analyze.c globals.h symtab.h analyze.h
	$(CC) -c analyze.c

lex.yy.o: tiny.l scan.h util.h globals.h
	$(LEX) 	tiny.l
	$(CC) -c lex.yy.c

tiny.tab.o: tiny.y globals.h
	$(BISON) -d tiny.y
	$(CC) -c tiny.tab.c

clean:
	-rm -f $(BIN)
	-rm -f tiny.tab.c
	-rm -f tiny.tab.h
	-rm -f lex.yy.c
	-rm -f $(OBJS)
