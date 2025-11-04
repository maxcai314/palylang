# palylang

The VM is based on a simplified version of RISC-V for simplicity. It should be
fairly simple to lower the instructions into real assembly.

The goal of this project is to compile programs into bytecodes for a lower-level
virtual machine, which can be interpreted, or eventually lowered into actual machine code.

This VM serves as a potential target platform for compilation as we explore programming language design.

## mathlang

Mathlang is a simple language with four arithmetic expressions over three integer registers.
It does not support any control flow modifications or external memory, and is therefore not Turing-complete.
Strictly speaking, mathlang is equivalent in power to a deterministic finite automaton (DFA), 
but it is still a programming language nonetheless.
Mathlang is intended as a basic introduction to lexing, parsing, and interpretation.
The files for mathlang are available in the `mathlang` folder.

Mathlang can be parsed and interpreted directly within python, or be compiled into our assembly language first
and then run using our VM.
