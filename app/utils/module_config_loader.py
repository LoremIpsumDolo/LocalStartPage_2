import json
from rich.console import Console

console = Console()


class ModuleConfigClass:

	def __init__(self):
		self.ConfigFilePath = "app/modules/module_configs.json"

	@property
	def ConfigFile(self) -> dict:
		"""
		opens the module config-file
		:return: config-data as dict
		"""

		with open(self.ConfigFilePath, "r") as file:
			return json.load(file)


	def updateConfigFile(self, new_config) -> None:

		console.log("updating module config")

		try:
			with open(self.ConfigFilePath, "w") as f:
				f.write(json.dumps(new_config,
				                   indent=4,
				                   ensure_ascii=True))

		except Exception as e:
			console.log(e)
