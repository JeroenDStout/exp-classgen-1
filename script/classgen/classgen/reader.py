from classgen_grammarVisitor import classgen_grammarVisitor
from . import types as classgen_types

class classgen_reader_visitor(classgen_grammarVisitor):
  def __init__(self, parser):
    self.parser       = parser
    self.current_enum = None
    self.indentation  = 0
    
  #
  #
  #
  def visitChildren(self, ctx):
    print(('  ' * self.indentation) + self.parser.ruleNames[ctx.getRuleIndex()])
    self.indentation += 1
    super().visitChildren(ctx)
    self.indentation -= 1
    
  def visitTerminal(self, ctx):
    print(('  ' * self.indentation) + '"' + ctx.getText() + '"')
    super().visitTerminal(ctx)