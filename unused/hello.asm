; nasm -felf64 ./hello.asm
; ld hello.o -o hello
%define SYS_EXIT 60

segment .text

global _start

_start:
	mov rax, SYS_EXIT ;; Syscall exit, dec 60
	mov rdi, 0 ;; Just to know we did it right
	syscall
	;ret ;; Possibly not needed return, since exit syscall will exit with status in rdi
