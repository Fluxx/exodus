class InvalidAdapterOption(Exception):
  pass

class Base(object):
  """Base adapter upon which all other interfaces must inherit from"""
  
  def __init__(self, database, options={}):
    """Returns a string of the command to run given the dictionary of __init__"""
    raise NotImplementedError( "Adapters must implement their own version of __init__()" )
        
class MySQL(Base):
  """MySQL migration runner adapter"""
  
  # Mapping of options passed in to the command() method to their command line name
  options_to_args = {
    "host": "--host",
    "user": "--user",
    "password": "--password"
  }
  
  def __init__(self, database, options={}):
    """Returns the MySQL command for the given set of options"""
    
    try:
      cmds = [ "%s=%s" % (self.options_to_args[k], v) for (k,v) in options.items() ]
      self.command = "mysql" + " ".join(cmds) + " " + database
    except KeyError as ke:
      raise InvalidAdapterOption("Option '%s' not valid" % ke)
      
  def load_file(self, filename):
    """Returns the command load a file in to MySQL"""
    return self.command + " < %s" % filename
    
  def add_migration(self, version):
    """Returns the command to add a migration to MySQL"""
    return self.command + " --command='INSERT INTO schema_migrations VALUES(%s)'" % version
    
  def remove_migration(self, version):
    """Returns the command to add a migration to MySQL"""
    return self.command + " --command='DELETE FROM schema_migrations WHERE version = %s'" % version
    
  def applied_migrations(self):
    """Returns the command to get the newline separated list of applied migrations"""
    return "%s | grep version | cut -d ' ' -f 2" % self.command
    
  def setup(self):
    """Returns the command to setup the migrations schema table"""
    return self.command + " --command=CREATE TABLE schema_migrations(version int NOT NULL)"