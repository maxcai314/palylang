# palylang

## Parsing
Build the ANTLR parser:
```
./palylang/parse/build.sh
```

Test it on some code:
```
python3 palylang/parse/Driver.py palylang/arithmetic_code.txt --dot palylang/arithmetic_code.dot
```
Render the dot file
```
dot -Tpng palylang/arithmetic_code.dot -o palylang/arithmetic_parse_tree.png
```
