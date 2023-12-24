import copy
from classgen_grammarVisitor import classgen_grammarVisitor
from . import tree  as classgen_tree
import copy
from . import types as classgen_types
  
#
#
#
class cg_reader_stack():
  class cg_context():
    def __init__(self):
      self.branch       = None
      self.current_enum = None
      
    def __str__(self):
      ret = "cg_context"
      if self.branch:
        ret += "\nbranch: " + str(self.branch)
      if self.current_enum:
        ret += "\nenum:   " + str(self.current_enum)
      return ret
  
  def __init__(self):
    context = self.cg_context()
    context.branch = classgen_tree.branch(None, "trunk")
    self.context_stack  = [ context ]
      
  def __str__(self):
    ret = "cg_reader_stack"
    idx = 0
    for elem in self.context_stack:
      ret += "\n[" + str(idx) + "] " + str(elem).replace("\n", "\n  ")
      idx += 1
    return ret
  
  def tail(self):
    return self.context_stack[-1]
  
  def push(self):
    self.context_stack.append(copy.copy(self.context_stack[-1]))
  
  def pop(self):
    self.context_stack.pop()
  
  def push_branch(self, symbolic_name):
    next_branch = classgen_tree.branch(self.tail().branch, symbolic_name)
    self.push()
    self.context_stack[-2].branch.branches.append(next_branch)
    self.context_stack[-1].branch = next_branch
  
  def push_typed_vertex(self, vertex):
    self.push_branch(vertex.identifier.canon_name)
    self.tail().branch.vertex = vertex
    
#
#
#
class cg_reader_visitor(classgen_grammarVisitor):
  def __init__(self, parser):
    self.context_stack = cg_reader_stack()
    self.context       = self.context_stack.tail()
    self.tree          = self.context.branch
    self.parser        = parser
    self.current_enum  = None
    self.indentation   = 0
    
  def interpret_identifier_name(self, ctx):
    if hasattr(ctx, "identifier_name"):
      ctx_sub = ctx.identifier_name()
      if ctx_sub is not None:
        return ctx_sub.getText()
    return None
    
  def interpret_identifier(self, identifier, ctx):
    identifier.canon_name = self.interpret_identifier_name(ctx)
        
    if hasattr(ctx, "identifier_with_alias"):
      ctx_sub = ctx.identifier_with_alias()
      if ctx_sub is not None:
        identifier.canon_name = ctx_sub.name.text
        for alias in ctx_sub.identifier_alias_list().IDENTIFIER():
          identifier.alias_local.append(alias.getText())
    
  #
  #
  #
  def interpret_intrinsic_type(self, ctx):
    t = classgen_types.cg_typedecl()
    t.abstract_type = classgen_types.cg_abstract_type.INTRINSIC

    if ctx.intrinsic_boolean():
      t.intrinsic_type = classgen_types.cg_intrinsic_gen_type.BOOL
    elif ctx.intrinsic_signed_integer():
      t.intrinsic_type = classgen_types.cg_intrinsic_spec_type()
      t.intrinsic_type.gen_type = classgen_types.cg_intrinsic_gen_type.INT
      t.intrinsic_type.bitsize  = int(ctx.intrinsic_signed_integer().getText()[1:])
      t.intrinsic_type.signed   = True
    elif ctx.intrinsic_unsigned_integer():
      t.intrinsic_type = classgen_types.cg_intrinsic_spec_type()
      t.intrinsic_type.gen_type = classgen_types.cg_intrinsic_gen_type.INT
      t.intrinsic_type.bitsize  = int(ctx.intrinsic_unsigned_integer().getText()[1:])
    else:
      t = None  

    return t
    
  #
  #
  #
  def visitEnum_declaration(self, ctx):  
    next_enum = classgen_types.cg_enum_description()
    self.interpret_identifier(next_enum.identifier, ctx.identifier_flex())
    
    self.context_stack.push_typed_vertex(next_enum)
    self.context_stack.tail().current_enum = next_enum
    super().visitEnum_declaration(ctx)
    self.context_stack.pop()
    
  def visitEnum_declaration_token_list_element(self, ctx):
    identifier = classgen_types.cg_identifier()
    self.interpret_identifier(identifier, ctx.identifier_pure())
    self.context_stack.tail().current_enum.canon_tokens.append(identifier.canon_name)
    
    for mapped in ctx.mapping_implied_implementation_statement():
      sub_identifier = classgen_types.cg_identifier()
      self.interpret_identifier(sub_identifier, mapped.identifier_pure())
      branch = self.context_stack.tail().branch.locate(sub_identifier.canon_name)
      mapped_value = classgen_types.cg_hc_map_description.mapped_value()
      mapped_value.src = identifier.canon_name
      mapped_value.dst = mapped.mapping_value().getText()
      branch.vertex.map.append(mapped_value)
    
  #
  #
  #
  def visitMapping_implied_declaration(self, ctx):
    next_map = classgen_types.cg_hc_map_description()
    self.interpret_identifier(next_map.identifier, ctx.identifier_flex())
    self.add_alias_local(next_map.identifier)
    
    next_map.from_type.set_symbol(self.context_stack.tail().branch.get_symbolic_path())
    
    mapped_to_type = ctx.mapping_mapped_to_type()
    if mapped_to_type.intrinsic():
      next_map.to_type = self.interpret_intrinsic_type(mapped_to_type.intrinsic())
    elif mapped_to_type.identifier_pure():
      branch = self.context_stack.tail().branch.locate(mapped_to_type.identifier_pure().getText())
      next_map.to_type.set_symbol(branch.get_symbolic_path())

    if ctx.mapping_default_value():
      mapped_value = classgen_types.cg_hc_map_description.mapped_value()
      mapped_value.src = None
      mapped_value.dst = ctx.mapping_default_value().mapping_value().getText()
      next_map.map.append(mapped_value)
      
    self.context_stack.push_typed_vertex(next_map)
    self.context_stack.pop()
    
  #
  #
  # 
  def add_alias_local(self, identifier:classgen_types.cg_identifier):
    for elem in identifier.alias_local:
      self.context_stack.tail().branch.alias_local[elem] = identifier.canon_name
    
  #
  #
  #
  def visitChildren(self, ctx):
    #print(('  ' * self.indentation) + self.parser.ruleNames[ctx.getRuleIndex()])
    self.indentation += 1
    super().visitChildren(ctx)
    self.indentation -= 1
    
  def visitTerminal(self, ctx):
    #print(('  ' * self.indentation) + '"' + ctx.getText() + '"')
    super().visitTerminal(ctx)