import unittest
import exodus
import platform
from collections import deque

class TestRunner(unittest.TestCase):

  def test_raises_exception_without_constructor(self):
    self.assertRaises(TypeError, (lambda: exodus.Runner()))
  
  def test_raises_exception_with_a_bad_adapter(self):
    self.assertRaises(ValueError, (lambda: exodus.Runner('junk')))
    
  def test_sets_adapter_with_new_instance_of_argument(self):
    runner = exodus.Runner(exodus.adapter.MySQL)
    self.assertEqual(runner.adapter.__class__, exodus.adapter.MySQL)
    
  def test_takes_migrations_folder(self):
    runner = exodus.Runner(exodus.adapter.MySQL, migrations_folder="/tmp")
    self.assertEqual(runner.migrations_folder, "/tmp")
    
  def test_raises_exception_if_migrations_folder_is_not_found(self):
    runner = lambda: exodus.Runner(exodus.adapter.MySQL, migrations_folder="/gooblygook")
    self.assertRaises(ValueError, runner)
    
  def test_migrations_returns_list(self):
    runner = exodus.Runner(exodus.adapter.MySQL, migrations_folder="./tests/migrations")
    self.assertIsInstance(runner.migrations, list)

  def test_migrations_returns_migrations_in_folder_in_chronological_order(self):
    runner = exodus.Runner(exodus.adapter.MySQL, migrations_folder="./tests/migrations")
    self.assertEqual(len(runner.migrations), 3)
    self.assertEqual(runner.migrations[0].id, '1298095972_add_pies_table')
    self.assertEqual(runner.migrations[1].id, '1298095980_add_cakes_table')
    self.assertEqual(runner.migrations[2].id, '1298095999_add_frostings_table')
    
        
  # TODO Available runner method
  # 
  # Assert migration is properly formed with a timestamp, down and up files.
  # run_migration - migrations that have been run
  # pending_migrations - migrations that have yet to run
  # current_version - current version of migrations run