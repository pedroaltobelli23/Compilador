#!/bin/bash

python3 main.py test/input.go
cd test/
nasm -f elf -o program.o input.asm
gcc -m32 -no-pie -o program program.o
./program