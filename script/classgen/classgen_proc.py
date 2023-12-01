import sys
import antlr4
import math

#print(sys.argv)

# add our antlr generated files path
sys.path.insert(0, sys.argv[1])

from classgen_grammarLexer   import classgen_grammarLexer
from classgen_grammarParser  import classgen_grammarParser
from classgen_grammarVisitor import classgen_grammarVisitor

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

class ClassgenVisitor(classgen_grammarVisitor):
  collected_string = ""
  collected_answer = []

  def visitExpr(self, ctx):
    if ctx.fn != None:
      self.collected_string += parser.symbolicNames[ctx.fn.type]
      self.collected_string += "("
      valRh = self.visitExpr(ctx.rh)
      self.collected_string += ")"
      
      if   ctx.fn.type == parser.SQRT:  ret = math.sqrt(valRh)
      elif ctx.fn.type == parser.SIN:   ret = math.sin(valRh)
      else: raise Exception("Unknown operand");
      
      self.collected_answer += [ parser.symbolicNames[ctx.fn.type] + " " + str(valRh) + " = " + str(ret) ]
      return ret
  
    if ctx.op != None:
      self.collected_string += "("
      valLh = self.visitExpr(ctx.lh)
      self.collected_string += " " + parser.symbolicNames[ctx.op.type] + " "
      valRh = self.visitExpr(ctx.rh)
      self.collected_string += ")"
      
      if   ctx.op.type == parser.PLUS:  ret = valLh  + valRh
      elif ctx.op.type == parser.MINUS: ret = valLh  - valRh
      elif ctx.op.type == parser.MULT:  ret = valLh  * valRh
      elif ctx.op.type == parser.DIV:   ret = valLh  / valRh
      elif ctx.op.type == parser.POW:   ret = valLh ** valRh
      else: raise Exception("Unknown operand");
      
      self.collected_answer += [ str(valLh) + " " + parser.symbolicNames[ctx.op.type] + " " + str(valRh) + " = " + str(ret) ]
      return ret
      
    if ctx.ex != None:
      return self.visitExpr(ctx.ex)
      
    if ctx.INT():
      self.collected_string += str(ctx.INT())
      return float(str(ctx.INT()))
      
    raise Exception("Unknown expression type");
        
tree    = parser.prog()
visitor = ClassgenVisitor()

print("Input: " + data)
visitor.visit(tree)
print("Interpretation: " + visitor.collected_string)
print('  ' + '\n  '.join(visitor.collected_answer))