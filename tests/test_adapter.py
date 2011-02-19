import unittest
import exodus

class TestAdapter(unittest.TestCase):
  
  def test_passes(self):
    pass
  
  # Adapter methods
  # 
  # 1. run(migration, direction=up) - runs a migration direction (up/down)
  # 2. set_version(version) - sets the migration version to a certain timestamp
  # 2. applied_migrations - chronologically sorted list of applied migations