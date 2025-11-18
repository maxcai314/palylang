# mathlang 2.0

This is an upgraded version of mathlang, which supports unlimited and arbitrary variables,
rather than the original default a, b, c.
There is one small type safety feature: variables must
be assigned before they can be used.

This language is still NOT Turing-complete.

## Parsing
The parser can be run via:
```
python3 mathlang2/parser.py mathlang2/example_code.txt
```

An example of rejected code:
```
python3 mathlang2/parser.py mathlang2/invalid_code.txt
```

## Interpretation
We have implemented a simple python interpreter which runs the program by operating 
on an internal state dictionary. It can be run via:
```
python3 mathlang2/interpreter.py mathlang2/example_code.txt
```


All code should be run from the root folder of this project.
