# This is the base class for all modules
class ModuleTemplate:

	def __init__(self, module_config):
		self.Config = module_config["config"]
		self.Settings = module_config["settings"]
