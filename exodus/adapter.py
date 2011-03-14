class InvalidAdapterOption(Exception):
  pass

class Base(object):
  """Base adapter upon which all other interfaces must inherit from"""
  
  def command(self, database, options={}):
    """Returns a string of the command to run given the dictionary of options"""
    raise NotImplementedError( "Adapters must implement their own version of command()" )
    
class MySQL(Base):
  """MySQL migration runner adapter"""
  
  # Mapping of options passed in to the command() method to their command line name
  options_to_args = {
    "host": "--host",
    "user": "--user",
    "password": "--password"
  }
  
  def __init__(self):
    self.bin = "mysql"
  
  def command(self, database, options={}):
    """Returns the MySQL command for the given set of options"""
    try:
      cmds = [ "%s=%s" % (self.options_to_args[k], v) for (k,v) in options.items() ]
      cmds.insert(0, self.bin)
      return " ".join(cmds) + " " + database
    except KeyError as ke:
      raise InvalidAdapterOption("Option '%s' not valid" % ke)