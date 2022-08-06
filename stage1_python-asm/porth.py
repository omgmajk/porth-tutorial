#!/usr/bin/env python3

import sys
import subprocess

iota_counter = 0

# Emulate enums from golang
def iota(reset=False):
    global iota_counter # global so we can reset it, if we put it outside of fun doesnt work

    if reset:
        iota_counter = 0
        
    result = iota_counter
    iota_counter += 1
    
    return result

# Assembly operations, enums
OP_PUSH = iota(True)
OP_PLUS = iota()
OP_MINUS = iota()
OP_DUMP = iota()
COUNT_OPS = iota() # total count


def push(x):
    return (OP_PUSH, x) # operation, value

def plus():
    return (OP_PLUS, ) # Single element tuple

def minus():
    return (OP_MINUS, )

def dump():
    return (OP_DUMP, )

def simulate_program(program):
    stack = []
    for op in program:
        assert COUNT_OPS == 4, "Exhaustive handling of operations in simulation."
        if op[0] == OP_PUSH:
            stack.append(op[1]) # PUSH instruction
        elif op[0] == OP_PLUS:
            a = stack.pop()
            b = stack.pop()
            stack.append(a + b) # ADD instruction
        elif op[0] == OP_MINUS:
            a = stack.pop()
            b = stack.pop()
            stack.append(b - a) # SUB instruction
        elif op[0] == OP_DUMP:
            a = stack.pop() # Just print results of stack
            print(a)
        else:
            assert False, "unreachable"
         
def compile_program(program, out_file_path):
    # Generate assembly
    with open(out_file_path, "w") as out:
        out.write("segment .text\n")
        # dump() - start
        out.write("dump:\n")
        out.write("    mov  r9, -3689348814741910323\n")
        out.write("    sub  rsp, 40\n")
        out.write("    mov  BYTE [rsp+31], 10\n")
        out.write("    lea  rcx, [rsp+30]\n")
        out.write(".L2:\n")
        out.write("    mov  rax, rdi\n")
        out.write("    lea  r8, [rsp+32]\n")
        out.write("    mul  r9\n")
        out.write("    mov  rax, rdi\n")
        out.write("    sub  r8, rcx\n")
        out.write("    shr  rdx, 3\n")
        out.write("    lea  rsi, [rdx+rdx*4]\n")
        out.write("    add  rsi, rsi\n")
        out.write("    sub  rax, rsi\n")
        out.write("    add  eax, 48\n")
        out.write("    mov  BYTE [rcx], al\n")
        out.write("    mov  rax, rdi\n")
        out.write("    mov  rdi, rdx\n")
        out.write("    mov  rdx, rcx\n")
        out.write("    sub  rcx, 1\n")
        out.write("    cmp  rax, 9\n")
        out.write("    ja   .L2\n")
        out.write("    lea  rax, [rsp+32]\n")
        out.write("    mov  edi, 1\n")
        out.write("    sub  rdx, rax\n")
        out.write("    xor  eax, eax\n")
        out.write("    lea  rsi, [rsp+32+rdx]\n")
        out.write("    mov  rdx, r8\n")
        out.write("    mov  rax, 1\n")  # Call write syscall
        out.write("    syscall\n")
        out.write("    add  rsp, 40\n")
        out.write("    ret\n")
        # dump() - end
        # _start() - start
        out.write("global _start\n")
        out.write("_start:\n")
        for op in program:
            assert COUNT_OPS == 4, "Exhaustive handling of ops in compilation"
            if op[0] == OP_PUSH:
                out.write("    ;; -- push --\n")
                out.write(f"    push  {op[1]}\n")
            elif op[0] == OP_PLUS:
                out.write("    ;; -- plus --\n")
                out.write("    pop  rax\n")
                out.write("    pop  rbx\n")
                out.write("    add  rax, rbx\n")
                out.write("    push rax\n")
            elif op[0] == OP_MINUS:
                out.write("    ;; -- minus --\n")
                out.write("    pop  rax\n")
                out.write("    pop  rbx\n")
                out.write("    sub  rbx, rax\n")
                out.write("    push rbx\n")
            elif op[0] == OP_DUMP:
                out.write("    ;; -- dump --\n")
                out.write("    pop  rdi\n")
                out.write("    call dump\n")
            else:
                assert False, "unreachable"
        out.write("    mov  rax, 60\n") # syscall for exit
        out.write("    mov  rdi, 0\n")
        out.write("    syscall\n")

# Push two numbers to stack and print, simple test case
program = [
    push(35), 
    push(34), 
    plus(), 
    dump(),
    push(420),
    dump(),
    push(10),
    push(9), 
    minus(), # Can't handle negative numbers at the moment, so order here matters
    dump()
]

def usage():
    print("Usage: porth <subcommand> [args]")
    print("     sim         Simulate the program")
    print("     com         Compile the program")

def call_cmd(cmd):
    print(" ".join(cmd))
    subprocess.call(cmd)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: No sucommand provided.")
        usage()
        exit(1)

    subcommand = sys.argv[1]

    if subcommand == "sim":
        simulate_program(program)
    elif subcommand == "com":
        compile_program(program, "output.asm")
        call_cmd(["nasm", "-felf64", "output.asm"])
        call_cmd(["ld", "output.o", "-o", "output"])
    else:
        print("Error: Unknown subcommand %s" % (subcommand))
        usage()
        exit(1)
