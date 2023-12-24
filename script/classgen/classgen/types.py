from ast import Pass
from enum import Enum

#
#
#
class cg_identifier:
  def __init__(self):
    self.canon_name  = None
    self.alias_local = []
    
  def __str__(self):
    ret = ""
  
    if self.canon_name != None:
      ret += self.canon_name
    else:
      ret += "#NAMELESS#"
      
    if len(self.alias_local) > 0:
      ret += ' aka ' + ', '.join(self.alias_local)
      
    return "<" + ret + ">"
  
  def get_symbolic_name(self):
    if self.canon_name != None:
      return self.canon_name
    return "NAMELESS"

#
#
#
class cg_abstract_type(Enum):
  NONE      = 0
  INTRINSIC = 1
  SYMBOL    = 2
  
class cg_intrinsic_gen_type(Enum):
  NONE      = 0
  BOOL      = 1
  INT       = 2
 
class cg_typedecl():
  def __init__(self):
    self.abstract_type  = cg_abstract_type.NONE
    self.intrinsic_type = None
    self.symbol_path    = None
    
  def __str__(self):
    match self.abstract_type:
      case cg_abstract_type.NONE:
        return "NONE"
      case cg_abstract_type.INTRINSIC:
        return str(self.intrinsic_type)
      case cg_abstract_type.SYMBOL:
        return "@" + "::".join(self.symbol_path)
    return "UNKNOWN"
  
  def set_symbol(self, symbol_path_list):
    self.abstract_type  = cg_abstract_type.SYMBOL
    self.symbol_path    = symbol_path_list
  
class cg_intrinsic_spec_type():
  def __init__(self):
    self.gen_type = cg_intrinsic_gen_type.NONE
    self.signed   = False
    self.bitsize  = 0

  @staticmethod
  def may_have_bitsize(gen_type:cg_intrinsic_gen_type):
    match gen_type:
      case cg_intrinsic_gen_type.INT:
        return True
      case _:
        return False
        
  def __str__(self):
    ret = str(self.gen_type)
    if self.may_have_bitsize(self.gen_type):
      ret += '$' + str(self.bitsize)
    return ret
  
class cg_typed_constant():
  def __init__(self):
    self.type  = cg_typedecl()
    self.value = None
    
  def __str__(self):
    return "(" + str(self.value) + " : " + str(self.type) + ")"

#
#
#
class cg_enum_description:
  def __init__(self):
    self.identifier = cg_identifier()
    self.canon_tokens = []
    
  def __str__(self):
    text = "enum_description " + str(self.identifier)
    text += "\n  [" + ", ".join(self.canon_tokens) + "]"
    return text

#
#
#
class cg_hc_map_description:
  class mapped_value:
    def __init__(self):
      self.src = None
      self.dst = None 

  def __init__(self):
    self.identifier = cg_identifier()
    self.from_type  = cg_typedecl()
    self.to_type    = cg_typedecl()
    self.map        = []
    
  def __str__(self):
    text = "cg_hc_map_description " + str(self.identifier)
    text += "\n  " + str(self.from_type) + " -> " + str(self.to_type)
    for value in self.map:
      text += "\n    " + str(value.src) + " -> " + str(value.dst)
    return text
