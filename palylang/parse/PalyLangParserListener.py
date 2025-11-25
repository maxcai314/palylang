# Generated from PalyLangParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PalyLangParser import PalyLangParser
else:
    from PalyLangParser import PalyLangParser

# This class defines a complete listener for a parse tree produced by PalyLangParser.
class PalyLangParserListener(ParseTreeListener):

    # Enter a parse tree produced by PalyLangParser#compilationUnit.
    def enterCompilationUnit(self, ctx:PalyLangParser.CompilationUnitContext):
        pass

    # Exit a parse tree produced by PalyLangParser#compilationUnit.
    def exitCompilationUnit(self, ctx:PalyLangParser.CompilationUnitContext):
        pass


    # Enter a parse tree produced by PalyLangParser#importDeclaration.
    def enterImportDeclaration(self, ctx:PalyLangParser.ImportDeclarationContext):
        pass

    # Exit a parse tree produced by PalyLangParser#importDeclaration.
    def exitImportDeclaration(self, ctx:PalyLangParser.ImportDeclarationContext):
        pass


    # Enter a parse tree produced by PalyLangParser#typeDeclaration.
    def enterTypeDeclaration(self, ctx:PalyLangParser.TypeDeclarationContext):
        pass

    # Exit a parse tree produced by PalyLangParser#typeDeclaration.
    def exitTypeDeclaration(self, ctx:PalyLangParser.TypeDeclarationContext):
        pass


    # Enter a parse tree produced by PalyLangParser#structDeclartion.
    def enterStructDeclartion(self, ctx:PalyLangParser.StructDeclartionContext):
        pass

    # Exit a parse tree produced by PalyLangParser#structDeclartion.
    def exitStructDeclartion(self, ctx:PalyLangParser.StructDeclartionContext):
        pass


    # Enter a parse tree produced by PalyLangParser#unionDeclaration.
    def enterUnionDeclaration(self, ctx:PalyLangParser.UnionDeclarationContext):
        pass

    # Exit a parse tree produced by PalyLangParser#unionDeclaration.
    def exitUnionDeclaration(self, ctx:PalyLangParser.UnionDeclarationContext):
        pass


    # Enter a parse tree produced by PalyLangParser#structBody.
    def enterStructBody(self, ctx:PalyLangParser.StructBodyContext):
        pass

    # Exit a parse tree produced by PalyLangParser#structBody.
    def exitStructBody(self, ctx:PalyLangParser.StructBodyContext):
        pass


    # Enter a parse tree produced by PalyLangParser#unionBody.
    def enterUnionBody(self, ctx:PalyLangParser.UnionBodyContext):
        pass

    # Exit a parse tree produced by PalyLangParser#unionBody.
    def exitUnionBody(self, ctx:PalyLangParser.UnionBodyContext):
        pass


    # Enter a parse tree produced by PalyLangParser#fieldDeclaration.
    def enterFieldDeclaration(self, ctx:PalyLangParser.FieldDeclarationContext):
        pass

    # Exit a parse tree produced by PalyLangParser#fieldDeclaration.
    def exitFieldDeclaration(self, ctx:PalyLangParser.FieldDeclarationContext):
        pass


    # Enter a parse tree produced by PalyLangParser#functionDeclaration.
    def enterFunctionDeclaration(self, ctx:PalyLangParser.FunctionDeclarationContext):
        pass

    # Exit a parse tree produced by PalyLangParser#functionDeclaration.
    def exitFunctionDeclaration(self, ctx:PalyLangParser.FunctionDeclarationContext):
        pass


    # Enter a parse tree produced by PalyLangParser#functionBody.
    def enterFunctionBody(self, ctx:PalyLangParser.FunctionBodyContext):
        pass

    # Exit a parse tree produced by PalyLangParser#functionBody.
    def exitFunctionBody(self, ctx:PalyLangParser.FunctionBodyContext):
        pass


    # Enter a parse tree produced by PalyLangParser#formalParameterList.
    def enterFormalParameterList(self, ctx:PalyLangParser.FormalParameterListContext):
        pass

    # Exit a parse tree produced by PalyLangParser#formalParameterList.
    def exitFormalParameterList(self, ctx:PalyLangParser.FormalParameterListContext):
        pass


    # Enter a parse tree produced by PalyLangParser#formalParameter.
    def enterFormalParameter(self, ctx:PalyLangParser.FormalParameterContext):
        pass

    # Exit a parse tree produced by PalyLangParser#formalParameter.
    def exitFormalParameter(self, ctx:PalyLangParser.FormalParameterContext):
        pass


    # Enter a parse tree produced by PalyLangParser#literal.
    def enterLiteral(self, ctx:PalyLangParser.LiteralContext):
        pass

    # Exit a parse tree produced by PalyLangParser#literal.
    def exitLiteral(self, ctx:PalyLangParser.LiteralContext):
        pass


    # Enter a parse tree produced by PalyLangParser#textLiteral.
    def enterTextLiteral(self, ctx:PalyLangParser.TextLiteralContext):
        pass

    # Exit a parse tree produced by PalyLangParser#textLiteral.
    def exitTextLiteral(self, ctx:PalyLangParser.TextLiteralContext):
        pass


    # Enter a parse tree produced by PalyLangParser#integerLiteral.
    def enterIntegerLiteral(self, ctx:PalyLangParser.IntegerLiteralContext):
        pass

    # Exit a parse tree produced by PalyLangParser#integerLiteral.
    def exitIntegerLiteral(self, ctx:PalyLangParser.IntegerLiteralContext):
        pass


    # Enter a parse tree produced by PalyLangParser#elementValue.
    def enterElementValue(self, ctx:PalyLangParser.ElementValueContext):
        pass

    # Exit a parse tree produced by PalyLangParser#elementValue.
    def exitElementValue(self, ctx:PalyLangParser.ElementValueContext):
        pass


    # Enter a parse tree produced by PalyLangParser#elementValueArrayInitializer.
    def enterElementValueArrayInitializer(self, ctx:PalyLangParser.ElementValueArrayInitializerContext):
        pass

    # Exit a parse tree produced by PalyLangParser#elementValueArrayInitializer.
    def exitElementValueArrayInitializer(self, ctx:PalyLangParser.ElementValueArrayInitializerContext):
        pass


    # Enter a parse tree produced by PalyLangParser#variableDeclarator.
    def enterVariableDeclarator(self, ctx:PalyLangParser.VariableDeclaratorContext):
        pass

    # Exit a parse tree produced by PalyLangParser#variableDeclarator.
    def exitVariableDeclarator(self, ctx:PalyLangParser.VariableDeclaratorContext):
        pass


    # Enter a parse tree produced by PalyLangParser#variableInitializer.
    def enterVariableInitializer(self, ctx:PalyLangParser.VariableInitializerContext):
        pass

    # Exit a parse tree produced by PalyLangParser#variableInitializer.
    def exitVariableInitializer(self, ctx:PalyLangParser.VariableInitializerContext):
        pass


    # Enter a parse tree produced by PalyLangParser#arrayInitializer.
    def enterArrayInitializer(self, ctx:PalyLangParser.ArrayInitializerContext):
        pass

    # Exit a parse tree produced by PalyLangParser#arrayInitializer.
    def exitArrayInitializer(self, ctx:PalyLangParser.ArrayInitializerContext):
        pass


    # Enter a parse tree produced by PalyLangParser#variableDeclaratorId.
    def enterVariableDeclaratorId(self, ctx:PalyLangParser.VariableDeclaratorIdContext):
        pass

    # Exit a parse tree produced by PalyLangParser#variableDeclaratorId.
    def exitVariableDeclaratorId(self, ctx:PalyLangParser.VariableDeclaratorIdContext):
        pass


    # Enter a parse tree produced by PalyLangParser#block.
    def enterBlock(self, ctx:PalyLangParser.BlockContext):
        pass

    # Exit a parse tree produced by PalyLangParser#block.
    def exitBlock(self, ctx:PalyLangParser.BlockContext):
        pass


    # Enter a parse tree produced by PalyLangParser#blockContent.
    def enterBlockContent(self, ctx:PalyLangParser.BlockContentContext):
        pass

    # Exit a parse tree produced by PalyLangParser#blockContent.
    def exitBlockContent(self, ctx:PalyLangParser.BlockContentContext):
        pass


    # Enter a parse tree produced by PalyLangParser#variableDeclaration.
    def enterVariableDeclaration(self, ctx:PalyLangParser.VariableDeclarationContext):
        pass

    # Exit a parse tree produced by PalyLangParser#variableDeclaration.
    def exitVariableDeclaration(self, ctx:PalyLangParser.VariableDeclarationContext):
        pass


    # Enter a parse tree produced by PalyLangParser#statement.
    def enterStatement(self, ctx:PalyLangParser.StatementContext):
        pass

    # Exit a parse tree produced by PalyLangParser#statement.
    def exitStatement(self, ctx:PalyLangParser.StatementContext):
        pass


    # Enter a parse tree produced by PalyLangParser#forControl.
    def enterForControl(self, ctx:PalyLangParser.ForControlContext):
        pass

    # Exit a parse tree produced by PalyLangParser#forControl.
    def exitForControl(self, ctx:PalyLangParser.ForControlContext):
        pass


    # Enter a parse tree produced by PalyLangParser#forCondition.
    def enterForCondition(self, ctx:PalyLangParser.ForConditionContext):
        pass

    # Exit a parse tree produced by PalyLangParser#forCondition.
    def exitForCondition(self, ctx:PalyLangParser.ForConditionContext):
        pass


    # Enter a parse tree produced by PalyLangParser#forUpdate.
    def enterForUpdate(self, ctx:PalyLangParser.ForUpdateContext):
        pass

    # Exit a parse tree produced by PalyLangParser#forUpdate.
    def exitForUpdate(self, ctx:PalyLangParser.ForUpdateContext):
        pass


    # Enter a parse tree produced by PalyLangParser#forInit.
    def enterForInit(self, ctx:PalyLangParser.ForInitContext):
        pass

    # Exit a parse tree produced by PalyLangParser#forInit.
    def exitForInit(self, ctx:PalyLangParser.ForInitContext):
        pass


    # Enter a parse tree produced by PalyLangParser#expressionList.
    def enterExpressionList(self, ctx:PalyLangParser.ExpressionListContext):
        pass

    # Exit a parse tree produced by PalyLangParser#expressionList.
    def exitExpressionList(self, ctx:PalyLangParser.ExpressionListContext):
        pass


    # Enter a parse tree produced by PalyLangParser#functionCall.
    def enterFunctionCall(self, ctx:PalyLangParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by PalyLangParser#functionCall.
    def exitFunctionCall(self, ctx:PalyLangParser.FunctionCallContext):
        pass


    # Enter a parse tree produced by PalyLangParser#MemberReferenceExpression.
    def enterMemberReferenceExpression(self, ctx:PalyLangParser.MemberReferenceExpressionContext):
        pass

    # Exit a parse tree produced by PalyLangParser#MemberReferenceExpression.
    def exitMemberReferenceExpression(self, ctx:PalyLangParser.MemberReferenceExpressionContext):
        pass


    # Enter a parse tree produced by PalyLangParser#BinaryOperatorExpression.
    def enterBinaryOperatorExpression(self, ctx:PalyLangParser.BinaryOperatorExpressionContext):
        pass

    # Exit a parse tree produced by PalyLangParser#BinaryOperatorExpression.
    def exitBinaryOperatorExpression(self, ctx:PalyLangParser.BinaryOperatorExpressionContext):
        pass


    # Enter a parse tree produced by PalyLangParser#UnaryOperatorExpression.
    def enterUnaryOperatorExpression(self, ctx:PalyLangParser.UnaryOperatorExpressionContext):
        pass

    # Exit a parse tree produced by PalyLangParser#UnaryOperatorExpression.
    def exitUnaryOperatorExpression(self, ctx:PalyLangParser.UnaryOperatorExpressionContext):
        pass


    # Enter a parse tree produced by PalyLangParser#PrimaryExpression.
    def enterPrimaryExpression(self, ctx:PalyLangParser.PrimaryExpressionContext):
        pass

    # Exit a parse tree produced by PalyLangParser#PrimaryExpression.
    def exitPrimaryExpression(self, ctx:PalyLangParser.PrimaryExpressionContext):
        pass


    # Enter a parse tree produced by PalyLangParser#SquareBracketExpression.
    def enterSquareBracketExpression(self, ctx:PalyLangParser.SquareBracketExpressionContext):
        pass

    # Exit a parse tree produced by PalyLangParser#SquareBracketExpression.
    def exitSquareBracketExpression(self, ctx:PalyLangParser.SquareBracketExpressionContext):
        pass


    # Enter a parse tree produced by PalyLangParser#CastExpression.
    def enterCastExpression(self, ctx:PalyLangParser.CastExpressionContext):
        pass

    # Exit a parse tree produced by PalyLangParser#CastExpression.
    def exitCastExpression(self, ctx:PalyLangParser.CastExpressionContext):
        pass


    # Enter a parse tree produced by PalyLangParser#FunctionCallExpression.
    def enterFunctionCallExpression(self, ctx:PalyLangParser.FunctionCallExpressionContext):
        pass

    # Exit a parse tree produced by PalyLangParser#FunctionCallExpression.
    def exitFunctionCallExpression(self, ctx:PalyLangParser.FunctionCallExpressionContext):
        pass


    # Enter a parse tree produced by PalyLangParser#PostIncrementDecrementOperatorExpression.
    def enterPostIncrementDecrementOperatorExpression(self, ctx:PalyLangParser.PostIncrementDecrementOperatorExpressionContext):
        pass

    # Exit a parse tree produced by PalyLangParser#PostIncrementDecrementOperatorExpression.
    def exitPostIncrementDecrementOperatorExpression(self, ctx:PalyLangParser.PostIncrementDecrementOperatorExpressionContext):
        pass


    # Enter a parse tree produced by PalyLangParser#primary.
    def enterPrimary(self, ctx:PalyLangParser.PrimaryContext):
        pass

    # Exit a parse tree produced by PalyLangParser#primary.
    def exitPrimary(self, ctx:PalyLangParser.PrimaryContext):
        pass


    # Enter a parse tree produced by PalyLangParser#typeType.
    def enterTypeType(self, ctx:PalyLangParser.TypeTypeContext):
        pass

    # Exit a parse tree produced by PalyLangParser#typeType.
    def exitTypeType(self, ctx:PalyLangParser.TypeTypeContext):
        pass


    # Enter a parse tree produced by PalyLangParser#declarableTypeType.
    def enterDeclarableTypeType(self, ctx:PalyLangParser.DeclarableTypeTypeContext):
        pass

    # Exit a parse tree produced by PalyLangParser#declarableTypeType.
    def exitDeclarableTypeType(self, ctx:PalyLangParser.DeclarableTypeTypeContext):
        pass


    # Enter a parse tree produced by PalyLangParser#primitiveType.
    def enterPrimitiveType(self, ctx:PalyLangParser.PrimitiveTypeContext):
        pass

    # Exit a parse tree produced by PalyLangParser#primitiveType.
    def exitPrimitiveType(self, ctx:PalyLangParser.PrimitiveTypeContext):
        pass


    # Enter a parse tree produced by PalyLangParser#identifier.
    def enterIdentifier(self, ctx:PalyLangParser.IdentifierContext):
        pass

    # Exit a parse tree produced by PalyLangParser#identifier.
    def exitIdentifier(self, ctx:PalyLangParser.IdentifierContext):
        pass


    # Enter a parse tree produced by PalyLangParser#arguments.
    def enterArguments(self, ctx:PalyLangParser.ArgumentsContext):
        pass

    # Exit a parse tree produced by PalyLangParser#arguments.
    def exitArguments(self, ctx:PalyLangParser.ArgumentsContext):
        pass



del PalyLangParser