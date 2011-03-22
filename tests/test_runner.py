import unittest
import exodus
import platform

from collections import deque

class DummyAdapter(exodus.adapter.Base):
  
  def __init__(self, database, options={}):
    pass
    
  def setup(self):
    raise NotImplementedError("setup")
    
  def load_file(self, file):
    raise NotImplementedError("load_file")
    
  def applied_migrations(self):
    raise NotImplementedError("applied_migrations")
        
class TestRunner(unittest.TestCase):

  def test_raises_exception_without_constructor(self):
    self.assertRaises(TypeError, (lambda: exodus.Runner()))
  
  def test_raises_exception_with_a_bad_adapter(self):
    self.assertRaises(ValueError, (lambda: exodus.Runner('badadapter', 'junk')))
    
  def test_raises_exception_if_migrations_folder_is_not_found(self):
    runner = lambda: exodus.Runner(exodus.adapter.MySQL, 'test', migrations_folder="/gooblygook")
    self.assertRaises(ValueError, runner)
    
  def test_sets_adapter_with_new_instance_of_argument(self):
    runner = exodus.Runner(exodus.adapter.MySQL, 'test', migrations_folder="./tests/migrations/valid")
    self.assertEqual(runner.adapter.__class__, exodus.adapter.MySQL)
    
  def test_takes_migrations_folder(self):
    runner = exodus.Runner(exodus.adapter.MySQL, 'test', migrations_folder="./tests/migrations/valid")
    self.assertEqual(runner.migrations_folder, "./tests/migrations/valid")
        
  def test_migrations_returns_list(self):
    runner = exodus.Runner(exodus.adapter.MySQL, 'test', migrations_folder="./tests/migrations/valid")
    self.assertIsInstance(runner.migrations, list)

  def test_migrations_returns_migrations_in_folder_in_chronological_order(self):
    runner = exodus.Runner(exodus.adapter.MySQL, 'test', migrations_folder="./tests/migrations/valid")
    self.assertEqual(len(runner.migrations), 3)
    self.assertEqual(runner.migrations[0].name, '1298095972_add_pies_table')
    self.assertEqual(runner.migrations[1].name, '1298095980_add_cakes_table')
    self.assertEqual(runner.migrations[2].name, '1298095999_add_frostings_table')
    
  def test_setup_calls_adapters_setup_method(self):
    runner = lambda: exodus.Runner(DummyAdapter, 'test', migrations_folder="./tests/migrations/valid").setup()
    self.assertRaisesRegexp(NotImplementedError, 'setup', runner)
    
  def test_run_calls_adapters_load_file_method(self):
    runner = lambda: exodus.Runner(DummyAdapter, 'test', migrations_folder="./tests/migrations/valid").run('1298095972')
    self.assertRaisesRegexp(NotImplementedError, 'load_file', runner)
    
  def test_run_with_bad_migration_raises_exception(self):
    runner = lambda: exodus.Runner(DummyAdapter, 'test', migrations_folder="./tests/migrations/valid").run('9876')
    self.assertRaises(exodus.InvalidMigrationError, runner)
    
  def test_applied_migrations_calls_adapters_applied_migrations_method(self):
    runner = lambda: exodus.Runner(DummyAdapter, 'test', migrations_folder="./tests/migrations/valid").applied_migrations()
    self.assertRaisesRegexp(NotImplementedError, 'applied_migrations', runner)
  
  def test_pending_migrations_calls_adapters_applied_migrations_method(self):
    runner = lambda: exodus.Runner(DummyAdapter, 'test', migrations_folder="./tests/migrations/valid").pending_migrations()
    self.assertRaisesRegexp(NotImplementedError, 'applied_migrations', runner)
    
  # def test_pending_migrations_returns_list_of_yet_applied_migrations(self):
  #   runner = exodus.Runner(DummyAdatperWithAppliedMigration, 'test', migrations_folder="./tests/migrations/valid")
  #   runner.pending_migrations()
  #   self.assertTrue(1 == 2)
        
  # TODO Available runner method
  # 
  # applied_migrations - migrations that have been run
  # pending_migrations - migrations that have yet to run
  # current_version - current version of migrations run