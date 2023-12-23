#
#
#
class cg_identifier:
  def __init__(self):
    self.canon_name = None
    self.alias      = []
    
  def __str__(self):
    ret = ""
  
    if self.canon_name != None:
      ret += self.canon_name
    else:
      ret += "#NAMELESS#"
      
    if len(self.alias) > 0:
      ret += ' aka [' + ', '.join(self.alias) + ']'
      
    return "<" + ret + ">"

#
#
#
class cg_enum_description:
  def __init__(self):
    self.identifier = cg_identifier()
    self.canon_tokens = []
    
  def __str__(self):
    text = "enum_description " + str(self.identifier) + "\n"
    text += "  ct:[" + ", ".join(self.canon_tokens) + "]\n"
    return text
    
  def set_enum_map(self, token, map_name, map_value):
    print(map_name + " : " + token + " -> " + str(map_value))