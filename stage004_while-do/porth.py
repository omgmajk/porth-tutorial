#!/usr/bin/env python3

import sys
import subprocess
import shlex
from os import path

iota_counter = 0

def iota(reset=False):
    global iota_counter # global so we can reset it, if we put it outside of fun doesnt work

    if reset:
        iota_counter = 0
        
    result = iota_counter
    iota_counter += 1
    
    return result

# Assembly operations
OP_PUSH = iota(True)
OP_PLUS = iota()
OP_MINUS = iota()
OP_EQUAL = iota()
OP_DUMP = iota()
OP_IF = iota()
OP_END = iota()
OP_ELSE = iota()
OP_DUP = iota()
OP_GT = iota() # Greater sign
COUNT_OPS = iota()

# TODO:
# OP_LT
# OP_DO
# OP_WHILE

# Returns "opcodes" in tuple form so we can work with them 
def push(x):
    return (OP_PUSH, x) # operation, value

def plus():
    return (OP_PLUS, ) # Single element tuple

def minus():
    return (OP_MINUS, )

def equal():
    return (OP_EQUAL, )

def dump():
    return (OP_DUMP, )

def iff():
    return (OP_IF, )

def end():
    return (OP_END, )

def elze():
    return (OP_ELSE, )

def dup():
    return (OP_DUP, )

def gt():
    return (OP_GT, )

# Simulate, or "run" the program without compiling
def simulate_program(program):
    stack = []
    ip = 0
    while ip < len(program):
        assert COUNT_OPS == 10, "Exhaustive handling of operations in simulation."
        op = program[ip]
        if op[0] == OP_PUSH:
            stack.append(op[1]) # PUSH instruction
            ip += 1
        elif op[0] == OP_PLUS:
            a = stack.pop()
            b = stack.pop()
            stack.append(a + b) # ADD instruction
            ip += 1
        elif op[0] == OP_MINUS:
            a = stack.pop()
            b = stack.pop()
            stack.append(b - a) # SUB instruction
            ip += 1
        elif op[0] == OP_EQUAL:
            a = stack.pop()
            b = stack.pop()
            stack.append(int(a == b)) # Returns boolean, cast to int
            ip += 1
        elif op[0] == OP_IF:
            a = stack.pop()
            if a == 0:
                # jump to end
                assert len(op) >= 2, "'if' instruction does not have reference to the end of it's block."
                ip = op[1]           # Remember to call crossreference_block() here to simulate
            else:
                ip += 1
        elif op[0] == OP_ELSE:
            assert len(op) >= 2, "'else' instruction does not have reference to the end of it's block." # Same
            ip = op[1]
        elif op[0] == OP_END:
            ip += 1
        elif op[0] == OP_DUMP:
            a = stack.pop() # Just print results of stack
            print(a)
            ip += 1
        elif op[0] == OP_DUP:
            a = stack.pop()
            stack.append(a)
            stack.append(a) # Push back on stack twice
            ip += 1
        elif op[0] == OP_GT:
            """ Commenting out my solution for now because I'm thinking like an idiot
            b = stack.pop() # I don't get why this is a problem but have to pop backwards
            a = stack.pop()
            stack.append(a if a > b else b) # This is a weird fcking ternary
            """
            a = stack.pop()
            b = stack.pop()
            stack.append(int(a < b))
            ip += 1
        else:
            assert False, "unreachable"

# Compile the program to assembly
def compile_program(program, out_file_path):
    # Generate assembly
    with open(out_file_path, "w") as out:
        # Boilerplate
        out.write("BITS 64\n")
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
        for ip in range(len(program)):
            op = program[ip] # Refactoring to be able to store values
            assert COUNT_OPS == 10, "Exhaustive handling of ops in compilation"
            if op[0] == OP_PUSH:
                out.write("    ;; -- push --\n")
                out.write(f"    push  {op[1]}\n")
            elif op[0] == OP_PLUS:
                out.write("    ;; -- plus --\n")
                out.write("    pop  rax\n")
                out.write("    pop  rbx\n")
                out.write("    add  rax, rbx\n") # Add two numbers present in rax, rbx
                out.write("    push rax\n")
            elif op[0] == OP_MINUS:
                out.write("    ;; -- minus --\n")
                out.write("    pop  rax\n")
                out.write("    pop  rbx\n")
                out.write("    sub  rbx, rax\n") # Sub rbx with rax
                out.write("    push rbx\n")
            elif op[0] == OP_EQUAL:
                out.write("    ;; -- equal --\n")
                out.write("    mov rcx, 0\n") # fill rcx with 0
                out.write("    mov rdx, 1\n") 
                out.write("    pop rax\n")
                out.write("    pop rbx\n")
                out.write("    cmp rax, rbx\n") 
                out.write("    cmove rcx, rdx\n") # Move 1 into rcx if rax and rbx are eql
                out.write("    push  rcx\n") # Push out result
            elif op[0] == OP_DUMP:
                out.write("    ;; -- dump --\n")
                out.write("    pop  rdi\n")
                out.write("    call dump\n") # Calls the dump function which calls write
            elif op[0] == OP_IF:
                out.write("    ;; -- if --\n")
                out.write("    pop  rax\n") # Pop current value ontop of stack
                out.write("    test rax, rax\n") # Check if equal to zero
                assert len(op) == 2, "From compilation: 'if' instruction does not have a reference to the end of it's block. Call crossreference_blocks()."
                out.write("    jz  addr_%d\n" % op[1]) # Jump to address available in op, if equal to zero
            elif op[0] == OP_ELSE:
                out.write("    ;; -- else --\n")
                assert len(op) >= 2, "From compilation: 'else' instruction does not have a reference to the end of it's block. Call crossreference_blocks()."
                out.write("     jmp  addr_%d\n" % op[1]) # Just jump to addr that sits in tuple
                out.write("addr_%d:\n" % (ip + 1)) # Addr that follows if
            elif op[0] == OP_END:
                out.write("addr_%d:\n" % ip) # End to jump to, not indented
            elif op[0] == OP_DUP:
                out.write("    ;; -- dup --\n")
                out.write("    pop  rax\n")
                out.write("    push rax\n") # Pop and push twice, like in simulation
                out.write("    push rax\n")
            elif op[0] == OP_GT:
                out.write("    ;; -- gt --\n")
                out.write("    mov rcx, 0\n")
                out.write("    mov rdx, 1\n")
                out.write("    pop rbx\n") # Pop different order from equal, because number order matters here
                out.write("    pop rax\n") # Mostly because how we add rcx and rdx in above order
                out.write("    cmp rax, rbx\n")
                out.write("    cmovg rcx, rdx\n")
                out.write("    push rcx\n")
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
    assert COUNT_OPS == 10, "Exhaustive op handling in parse_token_as_op"
    if word == '+':
        return plus()
    elif word == '-':
        return minus()
    elif word == '.':
        return dump()
    elif word == '=':
        return equal()
    elif word == 'if':
        return iff()
    elif word == 'end':
        return end()
    elif word == 'else':
        return elze()
    elif word == 'dup':
        return dup()
    elif word == '>':
        return gt()
    else:
        try:
            return push(int(word)) # Throws automatic error if can't parse.
        except ValueError as err:
            print("%s:%d:%d: %s" % (file_path, row, col, err)) 
            exit(1)

# Handling blocks
def crossreference_blocks(program):
    stack = []
    for ip in range(len(program)):
        op = program[ip]
        assert COUNT_OPS == 10, "Exhaustive handling of ops in crossreference_blocks."
                               # Keep in mind that not all of the ops needs to be handled
                               # here, just the ones that form blocks.
        if op[0] == OP_IF:
            stack.append(ip) # Current address to stack
        elif op[0] == OP_ELSE:
            if_ip = stack.pop()
            assert program[if_ip][0] == OP_IF, "'else' can only be used in if blocks"
            program[if_ip] = (OP_IF, ip + 1) # Current address, just like at end, +1 to skip else instruction itself so that we execute the else block because otherwise else just jumps to end
            stack.append(ip) # Keep track of the new block that just formed starting address
        elif op[0] == OP_END:
            block_ip = stack.pop() # Pop that address # Rewriting to cover whiles and such
            if program[block_ip][0] == OP_IF or program[block_ip][0] == OP_ELSE:
                program[block_ip] = (program[block_ip][0], ip) # Set to right tuple
            else:
                assert False, "'end' can only close if-else blocks for now."
    return program

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
        return [(file_path, row, col, token)
                for (row, line) in enumerate(f.readlines())
                for (col, token) in lex_line(line)]

# Load source code
def load_program_from_file(file_path):
    return crossreference_blocks([parse_token_as_op(token) for token in lex_file(file_path)])
    
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
    subcommand, *argv = argv # extract subcommand

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
        usage(compiler_name) # Changed this from program, program not implemented.
        exit(1)
