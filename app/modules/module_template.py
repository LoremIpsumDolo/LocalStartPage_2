# This is the base class for all modules
class ModuleTemplate:

	def __init__(self, module_config):

		if len(module_config["config"]) == 1:
			self.Config = module_config["config"][0]
		else:
			self.Config = module_config["config"]

		self.Settings = module_config["settings"]
