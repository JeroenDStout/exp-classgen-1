#
#
#
class branch():
  def __init__(self, parent_, symbolic_name):
    self.parent      = parent_
    self.symbol      = symbolic_name
    self.symbol_path = self.get_symbolic_path()
    self.vertex      = None
    self.tokens      = []
    self.branches    = []
    self.alias_local = {}
  
  def __str__(self):
    ret = self.symbol
    if self.vertex:
      ret += "\n# " + str(self.vertex).replace("\n", "\n  ")
    for token in self.tokens:
      ret += "\n* " + token
    for branch in self.branches:
      ret += "\n::" + str(branch).replace("\n", "\n  ")
    for k, v in self.alias_local.items():
      ret += "\n~ " + str(k) + " -> " + str(v)
    return ret
  
  def get_symbolic_path(self):
    if self.parent is not None:
      sb = self.parent.get_symbolic_path() + [ self.symbol ]
      return sb
    return []
  
  def locate_branch(self, symbol):
    return next((b for b in self.branches if b.symbol == symbol), None)
  
  def locate(self, symbol, path=[]):
    if len(path) > 0:
      rep_path = self.alias_local.get(path[0], path[0])
      
      ret = self.locate_branch(rep_path)
      if ret:
        ret = ret.locate(symbol, path[1:])
      if ret:
        return ret
      
      if self.parent:
        return self.parent.locate(symbol, path)
      
      return None
    
    rep_symbol = self.alias_local.get(symbol, symbol)
      
    if self.symbol == rep_symbol:
      return self
    
    ret = self.locate_branch(rep_symbol)
    if ret:
      return ret
    
    if self.parent:
      return self.parent.locate(symbol)
    
    return None
    