import sys
import antlr4
import math

#print(sys.argv)

# add our antlr generated files path
sys.path.insert(0, sys.argv[1])

from classgen_grammarLexer   import classgen_grammarLexer
from classgen_grammarParser  import classgen_grammarParser
from classgen_grammarVisitor import classgen_grammarVisitor

from classgen import reader as classgen_reader
from classgen import debug as classgen_debug

sys_arg = {}
for arg in sys.argv[2:]:
  data = arg.split(':', 1)
  if len(data) == 2:
    sys_arg[data[0]] = data[1]
    continue
  print("Badly formatted argument: \"" + arg + "\"")
  
with open(sys_arg["in"]) as file:
  data = file.read()
     
lexer  = classgen_grammarLexer(antlr4.InputStream(data))
stream = antlr4.CommonTokenStream(lexer)
parser = classgen_grammarParser(stream)

# debug
#for token in stream.getTokens(0, stream.getNumberOfOnChannelTokens()):
#  print(lexer.ruleNames[token.type - 1])
        
tree    = parser.prog()
visitor = classgen_reader.classgen_reader_visitor(parser)

visitor.visit(tree)
