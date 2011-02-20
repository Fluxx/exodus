import unittest
import exodus

class TestMigration(unittest.TestCase):

  def test_raises_exception_without_folder(self):
    self.assertRaises(TypeError, (lambda: exodus.Migration()))
    
  def test_raises_exception_with_impropery_formatted_migration(self):
    self.assertRaises(exodus.InvalidMigrationError, (lambda: exodus.Migration('gobblygook')))
    
  def test_raises_exception_with_non_existant_migration_folder(self):
    self.assertRaises(exodus.InvalidMigrationError, (lambda: exodus.Migration('/tmp/1298095000_add_unicorn_butter')))

  def test_raises_exception_with_migration_missing_up_file(self):
    self.assertRaises(exodus.InvalidMigrationError, (lambda: exodus.Migration('./tests/migrations/missing_up/1298095999_add_color_column')))