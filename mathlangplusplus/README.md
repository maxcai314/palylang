# mathlang++

This is a more advanced math language, which supports complex arithmetic.
Its expressions can be compiled to run on mathlang 2.0.

This language is still NOT Turing-complete.

## Lexing
The lexer can be run via:
```
python3 mathlangplusplus/lexer.py mathlangplusplus/example_code.txt
```

## Expression Parsing
Test parsing expressions with PEMDAS
```
python3 mathlangplusplus/expression_parser.py
```

## Parsing
Parses lines of actual mathlang++ code into statements
```
python3 mathlangplusplus/parser.py mathlangplusplus/example_code.txt
```

## Compiling
Compiles mathlang++ into mathlang2.0
```
python3 mathlangplusplus/compiler.py mathlangplusplus/example_code.txt mathlangplusplus/compiled_output.txt
```
For fun, try double compiling:
```
python3 mathlangplusplus/compiler.py mathlangplusplus/compiled_output.txt mathlangplusplus/double_compiled_output.txt
```

Run the output via:
```
python3 mathlang2/interpreter.py mathlangplusplus/compiled_output.txt
```
```
python3 mathlang2/interpreter.py mathlangplusplus/double_compiled_output.txt
```

All code should be run from the root folder of this project.
