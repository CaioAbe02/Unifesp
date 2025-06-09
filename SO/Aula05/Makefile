# Compilador e flags
CC = gcc
CFLAGS = -Wall -O2

# Lista de todos os arquivos .c
SRCS = $(wildcard *.c)

# Gera os nomes dos executáveis (sem .c)
TARGETS = $(SRCS:.c=)

# Regra padrão: compila todos os .c em seus respectivos executáveis
all: $(TARGETS)

# Regra genérica: compila cada .c em um executável com o mesmo nome
%: %.c
	$(CC) $(CFLAGS) -o $@ $<

# Limpeza: remove todos os executáveis
clean:
	rm -f $(TARGETS)

.PHONY: all clean
