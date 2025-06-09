#!/bin/bash
#Author: Joahannes B. D. da Costa <joahannes.costa@unifesp.br>

echo "Compilando e executando o Programa A"
gcc -o A ProgramaA.c && ./A

echo

echo "Compilando e executando o Programa B"
gcc -o B ProgramaB.c && ./B

# echo "Removendo os programas"
rm A
rm B
