; constantes
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0

segment .data

formatin: db "%d", 0
formatout: db "%d", 10, 0 ; newline, nul terminator
scanint: times 4 db 0 ; 32bits integer = 4 bytes

segment .bss  ; variaveis
res RESB 1
extern fflush
extern stdout

section .text
global main ; linux
extern scanf ; linux
extern printf ; linux
extern fflush ; linux
extern stdout ; linux

; subrotinas if/while
binop_je:
JE binop_true
JMP binop_false

binop_jg:
JG binop_true
JMP binop_false

binop_jl:
JL binop_true
JMP binop_false

binop_false:
MOV EAX, False  
JMP binop_exit
binop_true:
MOV EAX, True
binop_exit:
RET

main:

PUSH EBP ; guarda o base pointer
MOV EBP, ESP ; estabelece um novo base pointer

; codigo gerado pelo compilador abaixo



PUSH DWORD 0
MOV EAX, 5
MOV [EBP-4], EAX
PUSH DWORD 0
MOV EAX, 1
MOV [EBP-8], EAX
LOOP_20:
MOV EAX, [EBP-4]
PUSH EAX
MOV EAX, [EBP-8]
POP EBX
CMP EAX, EBX
CALL binop_jl
CMP EAX, False
JE EXIT_20
MOV EAX, [EBP-8]
PUSH EAX
PUSH formatout
CALL printf
ADD ESP, 8
MOV EAX, 1
PUSH EAX
MOV EAX, [EBP-8]
POP EBX
ADD EAX, EBX
MOV [EBP-8], EAX
JMP LOOP_20
EXIT_20:

; interrupcao de saida (default)

PUSH DWORD [stdout]
CALL fflush
ADD ESP, 4

MOV ESP, EBP
POP EBP

MOV EAX, 1
XOR EBX, EBX
INT 0x80