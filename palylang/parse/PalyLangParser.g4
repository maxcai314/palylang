
// $antlr-format alignTrailingComments true, columnLimit 150, minEmptyLines 1, maxEmptyLinesToKeep 1, reflowComments false, useTab false
// $antlr-format allowShortRulesOnASingleLine false, allowShortBlocksOnASingleLine true, alignSemicolons hanging, alignColons hanging

parser grammar PalyLangParser;

options {
    tokenVocab = PalyLangLexer;
}

// todo: update this one
compilationUnit
    : (
        importDeclaration
        | typeDeclaration
        | structDeclartion
        | functionDeclaration
        | variableDeclaration ';'
        | ';'
    )* EOF;

importDeclaration
    : IMPORT STRING_LITERAL ';'
    ;

typeDeclaration
    : structDeclartion
    | unionDeclaration
    ;

structDeclartion
    : STRUCT identifier structBody
    ;

unionDeclaration
    : UNION identifier unionBody
    ;

structBody
    : '{' fieldDeclaration* '}'
    ;

unionBody
    : '{' fieldDeclaration* '}'
    ;

fieldDeclaration
    : variableDeclaration ';'
    ;

functionDeclaration
    : typeType identifier formalParameterList functionBody
    ;

functionBody
    : block
    | ';'
    ;

formalParameterList
    : '(' (formalParameter (',' formalParameter)*)? ')'
    ;

formalParameter
    : typeType variableDeclaratorId
    ;

literal
    : integerLiteral
    | textLiteral
    | CHAR_LITERAL
    | NULL_LITERAL
    ;

textLiteral
    : STRING_LITERAL
    | TEXT_BLOCK
    ;

integerLiteral
    : DECIMAL_LITERAL
    | HEX_LITERAL
    | OCT_LITERAL
    | BINARY_LITERAL
    ;

// todo: idk if this is used
elementValue
    : expression
    | elementValueArrayInitializer
    ;

elementValueArrayInitializer
    : '{' (elementValue (',' elementValue)*)? ','? '}'
    ;

variableDeclarator
    : variableDeclaratorId ('=' variableInitializer)?
    ;

variableInitializer
    : arrayInitializer
    | expression
    ;

arrayInitializer
    : '{' (variableInitializer (',' variableInitializer)* ','?)? '}'
    ;

variableDeclaratorId : identifier;

// STATEMENTS / BLOCKS
block
    : '{' blockContent* '}'
    ;

blockContent
    : variableDeclaration ';'
    | statement
    ;

variableDeclaration
    : declarableTypeType variableDeclarator
    ;

statement
    : blockStatement = block
    | IF '(' expression ')' statement (ELSE statement)?
    | FOR '(' forControl ')' statement
    | WHILE '(' expression ')' statement
    | DO statement WHILE '(' expression ')' ';'
    | RETURN expression? ';'
    | BREAK ';'
    | CONTINUE ';'
    | statementExpression = expression ';'
    ;

forControl
    : forInit? ';' forCondition? ';' forUpdate?
    ;

forCondition: expression;

forUpdate : expression;

forInit
    : variableDeclaration
    | expression
    ;

// EXPRESSIONS

expressionList
    : expression (',' expression)*
    ;

functionCall
    : identifier arguments
    ;

expression
    // Level 16, Primary, array and member access
    : primary                                                       #PrimaryExpression
    | expression '[' expression ']'                                 #SquareBracketExpression
    | expression bop = '.' identifier                               #MemberReferenceExpression
    | functionCall                                                  #FunctionCallExpression

    // Level 15 Post-increment/decrement operators
    | expression postfix = ('++' | '--')                            #PostIncrementDecrementOperatorExpression

    // Level 14, Unary operators
    | prefix = ('+' | '-' | '++' | '--' | '~' | '!' | '@' | '$') expression   #UnaryOperatorExpression

    // Level 13 Cast and object creation
    | '(' typeType ')' expression                                   #CastExpression

    // Level 12 to 1, Remaining operators
    // Level 12, Multiplicative operators
    | expression bop = ('*' | '/' | '%') expression           #BinaryOperatorExpression
    // Level 11, Additive operators
    | expression bop = ('+' | '-') expression                 #BinaryOperatorExpression
    // Level 10, Shift operators
    | expression ('<' '<' | '>' '>' '>' | '>' '>') expression #BinaryOperatorExpression
    // Level 9, Relational operators
    | expression bop = ('<=' | '>=' | '>' | '<') expression   #BinaryOperatorExpression
    // Level 8, Equality Operators
    | expression bop = ('==' | '!=') expression               #BinaryOperatorExpression
    // Level 7, Bitwise AND
    | expression bop = '&' expression                         #BinaryOperatorExpression
    // Level 6, Bitwise XOR
    | expression bop = '^' expression                         #BinaryOperatorExpression
    // Level 5, Bitwise OR
    | expression bop = '|' expression                         #BinaryOperatorExpression
    // Level 4, Logic AND
    | expression bop = '&&' expression                        #BinaryOperatorExpression
    // Level 3, Logic OR
    | expression bop = '||' expression                        #BinaryOperatorExpression
    // Level 1, Assignment
    | <assoc = right> expression bop = (
        '='
        | '+='
        | '-='
        | '*='
        | '/='
        | '&='
        | '|='
        | '^='
        | '>>='
        | '>>>='
        | '<<='
        | '%='
    ) expression                                              #BinaryOperatorExpression
    ;

primary
    : '(' expression ')'
    | literal
    | identifier
    ;

typeType
    : (AT)* (identifier | primitiveType)
    ;

declarableTypeType
    : (AT)* (identifier | primitiveType) ('[' integerLiteral ']')*
    ; // can declare sized array variables

primitiveType
    : CHAR
    | SHORT
    | INT
    | LONG
    | VOID
    ;

identifier : IDENTIFIER;

arguments
    : '(' expressionList? ')'
    ;
