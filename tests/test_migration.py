import unittest
import exodus

class TestMigration(unittest.TestCase):

  def test_raises_exception_without_id(self):
    self.assertRaises(TypeError, (lambda: exodus.Migration()))