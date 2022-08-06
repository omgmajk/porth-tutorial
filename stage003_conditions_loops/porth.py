#!/usr/bin/env python3

import sys
import subprocess
import shlex # Simple lexical analysis
from os import path

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

# Call external programs and print a joined list
def call_echoed(cmd):
    print("[CMD] %s" % " ".join(map(shlex.quote, cmd)))
    subprocess.call(cmd)

# Print usage information
def usage(compiler_name):
    print("Usage: %s <subcommand> [args]" % compiler_name)
    print("     sim <file>        Simulate the program")
    print("     com <file>        Compile the program")
    print("     help              Print this help to stdout and exit with 0 code")

def parse_token_as_op(token):
    (file_path, row, col, word) = token # Destructuring an enumeration?
    assert COUNT_OPS == 4, "Exhaustive op handling in parse_token_as_op"
    if word == '+':
        return plus()
    elif word == '-':
        return minus()
    elif word == '.':
        return dump()
    else:
        try:
            return push(int(word)) # Throws automatic error if can't parse.
        except ValueError as err:
            print("%s:%d:%d: %s" % (file_path, row, col, err)) 
            exit(1)

# Lexer functions
def find_col(line, start, predicate):
    while start < len(line) and not predicate(line[start]):
        start += 1
    return start

def lex_line(line):
    col = find_col(line, 0, lambda x: not x.isspace()) # Advance until no space found
    while col < len(line):
        col_end = find_col(line, col, lambda x: x.isspace()) # Advance until space found
        yield (col, line[col:col_end]) # Partial return, interesting
        col = find_col(line, col_end, lambda x: not x.isspace()) # Keep advancing until next space

def lex_file(file_path):
    with open(file_path, "r") as f:
        return[(file_path, row, col, token)
            for (row, line) in enumerate(f.readlines())
            for (col, token) in lex_line(line)]

# Load source code
def load_program_from_file(file_path):
    return [parse_token_as_op(token) for token in lex_file(file_path)]
    
if __name__ == '__main__':
    argv = sys.argv

    assert len(argv) >= 1, "Error, sys.argv is not picking up input"

    # Check uncons method from lesson 1 for doing this with tuples
    # Apparently this works too?

    compiler_name, *argv = argv
    # Check
    if len(argv) < 1:
        print("Error: No subcommand provided.")
        usage(compiler_name)
        exit(1)
    # Parse rest
    subcommand, *argv = argv# extract subcommand

    if subcommand == "sim":
        if len(argv) < 1:
            usage(compiler_name)
            print("Error: No input file provided for the simulation")
            exit(1)
        program_path, *argv = argv # extract file to input
        program = load_program_from_file(program_path)
        simulate_program(program)
    elif subcommand == "com":
        if len(argv) < 1:
            usage(compiler_name)
            print("Error: No input file provided for the compiler")
            exit(1)
        program_path, *argv = argv
        program = load_program_from_file(program_path)
        porth_ext = '.porth'
        basename = path.basename(program_path)
        if basename.endswith(porth_ext):
            basename = basename[:-len(porth_ext)]
        print("[INFO] Generating %s" % (basename + ".asm"))
        compile_program(program, basename + ".asm")
        call_echoed(["nasm", "-felf64", basename + ".asm"])
        call_echoed(["ld", basename + ".o", "-o", basename])
    elif subcommand == "help":
        usage(compiler_name)
        exit(0)
    else:
        print("Error: Unknown subcommand %s" % (subcommand))
        usage(program)
        exit(1)
