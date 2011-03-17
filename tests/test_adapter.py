import unittest
import exodus

class TestAdapter(unittest.TestCase):
  
  def test_base_adapter_command_method_raises_exception(self):
    self.assertRaises(NotImplementedError, (lambda: exodus.adapter.Base('test')))

# TODO: Add a helper to verify commands are between "mysql" and "database"
class TestMySQLAdapter(unittest.TestCase):
    
  def test_constructor_raises_exception_without_database(self):
    self.assertRaises(TypeError, lambda: exodus.adapter.MySQL())
  
  def test_command_has_mysql_bin(self):
    self.assertRegexpMatches(exodus.adapter.MySQL('test').command, "^mysql")
    
  def test_constructor_has_database_at_end(self):
    self.assertRegexpMatches(exodus.adapter.MySQL('test').command, "test$")
    
  def test_unsupported_option_raises_invalid_option_exception(self):
    command = lambda: exodus.adapter.MySQL('test', {'foo':'bar'}).command
    self.assertRaises(exodus.adapter.InvalidAdapterOption, command)
  
  def test_constructor_with_host_returns_correct_string(self):
    cmd = exodus.adapter.MySQL('test', {'host':'example.com'}).command
    self.assertRegexpMatches(cmd, "--host=example.com")
    
  def test_constructor_with_username_returns_correct_string(self):
    cmd = exodus.adapter.MySQL('test', {'host':'example.com'}).command
    self.assertRegexpMatches(cmd, "--host=example.com")
  
  def test_constructor_with_password_returns_correct_string(self):
    cmd = exodus.adapter.MySQL('test', {'password':'1234'}).command
    self.assertRegexpMatches(cmd, "--password=1234")
    
  def test_constructor_with_user_returns_correct_string(self):
    cmd = exodus.adapter.MySQL('test', {'user':'joe'}).command
    self.assertRegexpMatches(cmd, "--user=joe")
    

  
  # Adapter methods
  # 1. load_file(file) - loads a file via the command
  # 2. add_migration(version) - adds a migration as being run
  # 3. remove_migration(version) - removes a migration as being run
  # 4. applied_migrations - chronologically sorted list of applied migations
  # 5. setup - creates schema_migrations table in data store