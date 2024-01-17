import sys
from antlr4 import *
from compiler.grammar.WhileLexer import WhileLexer
from compiler.grammar.WhileParser import WhileParser
from compiler.grammar.WhileVisitor import WhileVisitor
from compiler.While3Addr import *
import logging
import compiler.util

class IRGenerator(WhileVisitor):
    """A visitor that compiles the While language into While three-address
code.  Statements visitors return nothing, while expression visitors
return the name of a variable that will hold the expression's value at
runtime."""

    # PROJECT: implement the IR generation
    
    def __init__(self, prog):
        self.prog = prog

    # Visit a parse tree produced by WhileParser#Assignment.
    def visitAssignment(self, ctx:WhileParser.AssignmentContext):
        # TODO
        return None

    # Visit a parse tree produced by WhileParser#Skip.
    def visitSkip(self, ctx:WhileParser.SkipContext):
        # do nothing
        return None

    # Visit a parse tree produced by WhileParser#If.
    def visitIf(self, ctx:WhileParser.IfContext):
        # TODO
        return None

    # Visit a parse tree produced by WhileParser#While.
    def visitWhile(self, ctx:WhileParser.WhileContext):
        # TODO
        return None

    # Visit a parse tree produced by WhileParser#Compound.
    def visitCompound(self, ctx:WhileParser.CompoundContext):
        # do nothing, except visit all nested statements
        self.visitChildren(ctx)
        return None

    # Visit a parse tree produced by WhileParser#Not.
    def visitNot(self, ctx:WhileParser.NotContext):
        # TODO
        return ""

    # Visit a parse tree produced by WhileParser#BOp.
    def visitBOp(self, ctx:WhileParser.BOpContext):
        # TODO
        return ""

    # Visit a parse tree produced by WhileParser#ROp.
    def visitROp(self, ctx:WhileParser.ROpContext):
        # TODO
        return ""

    # Visit a parse tree produced by WhileParser#True.
    def visitTrue(self, ctx:WhileParser.TrueContext):
        # TODO
        return ""

    # Visit a parse tree produced by WhileParser#False.
    def visitFalse(self, ctx:WhileParser.FalseContext):
        # TODO
        return ""

    # Visit a parse tree produced by WhileParser#BParen.
    def visitBParen(self, ctx:WhileParser.BParenContext):
        # TODO
        return ""

    # Visit a parse tree produced by WhileParser#AOp.
    def visitAOp(self, ctx:WhileParser.AOpContext):
        # TODO
        return ""

    # Visit a parse tree produced by WhileParser#Var.
    def visitVar(self, ctx:WhileParser.VarContext):
        # TODO
        return ""

    # Visit a parse tree produced by WhileParser#Num.
    def visitNum(self, ctx:WhileParser.NumContext):
        # TODO
        return ""

    # Visit a parse tree produced by WhileParser#AParen.
    def visitAParen(self, ctx:WhileParser.AParenContext):
        # do nothing except visit the expression inside the parentheses
        return self.visit(ctx.a())

def while2ir(input_stream):
    lexer = WhileLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = WhileParser(stream)
    tree = parser.s()
    if parser.getNumberOfSyntaxErrors() > 0:
        print("syntax errors")
        exit(1)
    else:
        program = Program()
        translator = IRGenerator(program)
        translator.visit(tree)
        return program
      
def main():
    import sys
    if len(sys.argv) > 1:
        input_stream = FileStream(sys.argv[1])
    else:
        input_stream = StdinStream()
    program = while2ir(input_stream)
    print(program)

if __name__ == '__main__':
    main()
