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

# Assembly operations, enums, sort of
OP_PUSH = iota(True)
OP_PLUS = iota()
OP_MINUS = iota()
OP_DUMP = iota()
COUNT_OPS = iota() # total count

# Returns "opcodes" in tuple form so we can work with them 
def push(x):
    return (OP_PUSH, x) # operation, value

def plus():
    return (OP_PLUS, ) # Single element tuple

def minus():
    return (OP_MINUS, )

def dump():
    return (OP_DUMP, )

# Simulate, or "run" the program without compiling
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

# Compile the program to assembly
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

# Print usage information
def usage(program):
    print("Usage: %s <subcommand> [args]" % program)
    print("     sim <file>        Simulate the program")
    print("     com <file>        Compile the program")

# Call external programs and print a joined list
def call_cmd(cmd):
    print(" ".join(cmd))
    subprocess.call(cmd)

def parse_word_as_op(word):
    assert COUNT_OPS == 4, "Exhaustive op handling in parse_word_as_op"
    if word == '+':
        return plus()
    elif word == '-':
        return minus()
    elif word == '.':
        return dump()
    else:
        return push(int(word)) # Throws automatic error if can't parse.

# Load source code
def load_program_from_file(file_path):
    with open(file_path, "r") as f:
        # List comprehension, parse into operation, as split into words by split()
        # Trims \n automatically
        return [parse_word_as_op(word) for word in f.read().split()]

# Returns two arguments in a tuple, shifting away the first list item
def uncons(xs):
    return (xs[0], xs[1:])

if __name__ == '__main__':
    argv = sys.argv

    assert len(argv) >= 1, "Error, sys.argv is not picking up input"

    #argv = argv[1:] # pop / remove the program name "porth.py"
    (program_name, argv) = uncons(argv)
    # Check
    if len(argv) < 1:
        print("Error: No subcommand provided.")
        usage(program_name)
        exit(1)
    # Parse rest
    (subcommand, argv) = uncons(argv) # extract subcommand

    if subcommand == "sim":
        if len(argv) < 1:
            usage(program_name)
            print("Error: No input file provided for the simulation")
            exit(1)
        (program_path, argv) = uncons(argv) # extract file to input
        program = load_program_from_file(program_path)
        simulate_program(program)
    elif subcommand == "com":
        if len(argv) < 1:
            usage(program_name)
            print("Error: No input file provided for the compiler")
            exit(1)
        (program_path, argv) = uncons(argv)
        program = load_program_from_file(program_path)
        compile_program(program, "output.asm")
        call_cmd(["nasm", "-felf64", "output.asm"])
        call_cmd(["ld", "output.o", "-o", "output"])
    else:
        print("Error: Unknown subcommand %s" % (subcommand))
        usage(program)
        exit(1)
