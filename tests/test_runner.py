import unittest
import exodus

class TestRunner(unittest.TestCase):

  def test_raises_exception_without_constructor(self):
    self.assertRaises(TypeError, (lambda: exodus.Runner()))
  
  def test_raises_exception_with_a_bad_adapter(self):
    self.assertRaises(ValueError, (lambda: exodus.Runner('junk')))
    
  def test_sets_adapter_with_new_instance_of_argument(self):
    runner = exodus.Runner(exodus.adapter.MySQL)
    self.assertEqual(runner.adapter.__class__, exodus.adapter.MySQL)