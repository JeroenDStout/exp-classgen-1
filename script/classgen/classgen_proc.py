import sys
import antlr4

# add our antlr generated files path
sys.path.insert(0, sys.argv[1])

from classgen_grammarLexer    import classgen_grammarLexer
from classgen_grammarListener import classgen_grammarListener
from classgen_grammarParser   import classgen_grammarParser

print(sys.argv[2:])