import adapter
import os
from collections import deque

class Migration(object):
  """Migration to run"""
  
  def __init__(self, id):
    self.id = id

class Runner(object):
  """Analyzes migration status and runs the migrations"""

  def __init__(self, adptr, migrations_folder=os.getcwd()):
    if not adptr in adapter.Base.__subclasses__():
      raise ValueError("Adapter not supported")
      
    self.adapter = adptr()
    
    if not os.path.isdir(migrations_folder):
      raise ValueError("Migrations folder does not exist")
  
    self.migrations_folder = migrations_folder
    self.load_migrations()
    
  def load_migrations(self):
    """Loads migrations from the migrations path"""
    migration_folders = deque(os.listdir(self.migrations_folder))
    self.migrations = [ Migration(folder) for folder in migration_folders ]