#!/bin/sh

set -xe

nasm -felf64 hello.asm
ld hello.o -o hello
