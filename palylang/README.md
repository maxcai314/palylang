# palylang

## Parsing
Build the ANTLR parser:
```
./palylang/parse/build.sh
```

Test it on some code:
```
python3 palylang/parse/Driver.py palylang/example_code.txt --dot palylang/example_parse_tree.dot
```
Render the dot file
```
dot -Tpng palylang/example_parse_tree.dot -o palylang/example_parse_tree.png
```
