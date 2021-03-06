import adapter
import os
import re
import subprocess

from collections import deque

class Migration(object):
  """Migration to run"""
  
  def __init__(self, folder):
    self.folder = folder
    self.name = os.path.basename(folder)
    
    self.validate()
    self.version = int(self.name.partition('_')[0])
        
  def validate(self):
    """Is the migration valid or not"""
    
    if not re.match('\d{10,}_\w+', self.name):
      raise InvalidMigrationError("Migration %s not formatted correctly" % self.name)
    
    if not os.path.exists(self.folder):
      raise InvalidMigrationError("Migration folder %s does not exist" % self.folder)
    
    if not [ file for file in os.listdir(self.folder) if re.match('up', file) ]:
      raise InvalidMigrationError("Migration %s does not contain up file" % self.name)
        
class InvalidMigrationError(Exception):
  pass

class Runner(object):
  """Analyzes migration status and runs the migrations"""

  def __init__(self, adptr, database, migrations_folder=os.getcwd(), options={}):
    if not adptr in adapter.Base.__subclasses__():
      raise ValueError("Adapter %s not supported" % str(adptr))
    
    # Pass the database string and options dictionary to the specified adapter
    self.adapter = adptr(database, options)
    
    if not os.path.isdir(migrations_folder):
      raise ValueError("Migrations folder %s does not exist" % migrations_folder)
  
    self.migrations_folder = migrations_folder
    self.load_migrations()
    
  def load_migrations(self):
    """Loads migrations from the migrations path"""
    migration_folders = os.listdir(self.migrations_folder)
    self.migrations = [ Migration(os.path.join(self.migrations_folder, folder)) 
      for folder in migration_folders ]
      
  def setup(self):
    """Sets up the migration tracking table"""
    subprocess.check_output(self.adapter.setup())
    
  def run(self, migration, direction="up"):
    """Runs a specified migration"""
    
    if not int(migration) in [ migration.version for migration in self.migrations]:
      raise InvalidMigrationError("Migration %s not found" % migration)
    
    return subprocess.check_output(self.adapter.load_file("migration%s.sql" % direction))
    
  def applied_migrations(self):
    """Returns the applied migrations"""
    return subprocess.check_output(self.adapter.applied_migrations())
    
  def pending_migrations(self):
    """Returns the migrations which are still pending"""
    applied_migrations = self.applied_migrations()