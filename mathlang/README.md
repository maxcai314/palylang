# mathlang

A toy language to demonstrate basic compiler concepts.
This language is NOT Turing-complete.

```
Here are the rules of my simple language:
There are only three predefined variables: a, b, c
A line of code may contain a statement and/or a comment
There is only one type of statement: assignment
<lhs> = <rhs>
The left-hand side of assignment must be a variable name
The right-hand side is an expression
Expressions are either arithmetic operations, variable names, or literal numbers
The two sides of an arithmetic operation can be a variable name or a literal
+, -, *, /
a = 15 - a  # lol
```

You can run the compiler via:
```
python3 mathlang/mathlang_compiler.py mathlang/example_code.txt mathlang/mathlang_output.txt
```

And then run the outputted program via:
```
python3 interpreter.py mathlang/mathlang_output.txt
```

All code should be run from the root folder of this project.
