import unittest
import exodus

class TestAdapter(unittest.TestCase):
  
  def test_base_adapter_command_method_raises_exception(self):
    self.assertRaises(NotImplementedError, (lambda: exodus.adapter.Base('test')))
    
  def test_base_adapter_load_file_raises_exception(self):
    cmd = lambda: exodus.adapter.Base('test').load_file('upsql')
    self.assertRaises(NotImplementedError, cmd)
    
  def test_base_adapter_add_migration_raises_exception(self):
    cmd = lambda: exodus.adapter.Base('test').add_migration(1234567890)
    self.assertRaises(NotImplementedError, cmd)
  
  def test_base_adapter_remove_migration_raises_exception(self):
    cmd = lambda: exodus.adapter.Base('test').remove_migration(1234567890)
    self.assertRaises(NotImplementedError, cmd)

    def test_base_adapterapplied_migrations_raises_exception(self):
      cmd = lambda: exodus.adapter.Base('test').applied_migrations
      self.assertRaises(NotImplementedError, cmd)


# TODO: Add a helper to verify commands are between "mysql" and "database"
class TestMySQLAdapter(unittest.TestCase):
    
  def test_command_raises_exception_without_database(self):
    self.assertRaises(TypeError, lambda: exodus.adapter.MySQL())
  
  def test_command_has_mysql_bin(self):
    self.assertRegexpMatches(exodus.adapter.MySQL('test').command, "^mysql")
    
  def test_command_has_database_at_end(self):
    self.assertRegexpMatches(exodus.adapter.MySQL('test').command, "test$")
    
  def test_unsupported_option_raises_invalid_option_exception(self):
    command = lambda: exodus.adapter.MySQL('test', {'foo':'bar'}).command
    self.assertRaises(exodus.adapter.InvalidAdapterOption, command)
  
  def test_command_with_host_returns_correct_string(self):
    cmd = exodus.adapter.MySQL('test', {'host':'example.com'}).command
    self.assertRegexpMatches(cmd, "--host=example.com")
    
  def test_command_with_username_returns_correct_string(self):
    cmd = exodus.adapter.MySQL('test', {'host':'example.com'}).command
    self.assertRegexpMatches(cmd, "--host=example.com")
  
  def test_command_with_password_returns_correct_string(self):
    cmd = exodus.adapter.MySQL('test', {'password':'1234'}).command
    self.assertRegexpMatches(cmd, "--password=1234")
    
  def test_command_with_user_returns_correct_string(self):
    cmd = exodus.adapter.MySQL('test', {'user':'joe'}).command
    self.assertRegexpMatches(cmd, "--user=joe")
    
  def test_load_file_puts_filename_at_end(self):
    cmd = exodus.adapter.MySQL('test').load_file("up.sql")
    self.assertRegexpMatches(cmd, "< up.sql$")
    
  def test_add_migration_executes_an_insert(self):
    cmd = exodus.adapter.MySQL('test').add_migration(1234567890)
    self.assertRegexpMatches(cmd, "--command='INSERT INTO schema_migrations VALUES\(1234567890\)'$")
  
  def test_remove_migration_executes_an_insert(self):
    cmd = exodus.adapter.MySQL('test').remove_migration(1234567890)
    self.assertRegexpMatches(cmd, "--command='DELETE FROM schema_migrations WHERE version = 1234567890'$")
    
  def test_applied_migrations_greps_for_version(self):
    cmd = exodus.adapter.MySQL('test').applied_migrations()
    self.assertRegexpMatches(cmd, "| grep version")

  def test_applied_migrations_cuts_out_the_applied_migration(self):
    cmd = exodus.adapter.MySQL('test').applied_migrations()
    self.assertRegexpMatches(cmd, "| cut -d ' ' -f 2")
  
  # Adapter methods
  # 5. setup - creates schema_migrations table in data store