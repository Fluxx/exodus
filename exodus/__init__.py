import adapter

class Runner(object):
  """Analyzes migration status and runs the migrations"""

  def __init__(self, desired):
    if not desired in adapter.Base.__subclasses__():
      raise ValueError("Adapter not supported")
      
    self.adapter = desired()