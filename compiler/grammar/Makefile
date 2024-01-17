all: WhileParser.py

WhileParser.py:	While.g4
	java org.antlr.v4.Tool -visitor -Dlanguage=Python3 $<

clean:
	rm -f While.interp WhileLexer.interp WhileLexer.py WhileLexer.tokens WhileListener.py WhileParser.py WhileVisitor.py While.tokens
