import datetime
import importlib
import importlib.util
import json
import logging
import os

from rich.pretty import pprint

logger = logging.getLogger(__name__)


class ModuleHandlerClass:

	def __init__(self, database):
		self.database = database
		self.ConfigFilePath = "app/modules/module_configs.json"
		self.Modules = {}


	@property
	def Config(self) -> dict:
		"""
		opens the module config-file
		:return: config-data as dict
		"""

		with open(self.ConfigFilePath, "r") as file:
			return json.load(file)


	def ModuleConfig(self, module_name):
		return self.Config[module_name]


	def update_ConfigFile(self, new_config) -> None:

		logger.info("updating module config")

		try:
			with open(self.ConfigFilePath, "w") as f:
				f.write(json.dumps(new_config,
				                   indent=4,
				                   ensure_ascii=True))

		except Exception as e:
			logger.error(e)


	def showConfigFile(self) -> None:
		pprint(self.Config, expand_all=True)


	def get_active_Modules(self) -> list:
		"""
		Returns a list of all active modules
		:return: A list of the active modules.
		"""

		module_files = [filename.split(".")[0] for filename in os.listdir("app/modules")]

		return [
				module for module in self.Config.keys()
				if self.Config[module]["settings"]["active"] == "True"
				   and self.Config[module]["settings"]["module_name"] in module_files
				]


	def import_active_Modules(self) -> list:
		"""
		Import all active modules from the config file
		"""

		for module_name in self.get_active_Modules():

			_module_name = module_name

			full_path_to_module = f'app/modules/{self.Config[module_name]["settings"]["module_name"]}.py'
			module_classname = self.Config[module_name]["settings"]["module_classname"]

			try:
				module_dir, module_file = os.path.split(full_path_to_module)
				module_name, module_ext = os.path.splitext(module_file)

				# Get module "spec" from filename
				spec = importlib.util.spec_from_file_location(module_name, full_path_to_module)
				module = spec.loader.load_module()

			except Exception as e:
				raise ImportError(e) from e

			self.Modules[module_classname] = module.ModuleClass(self.ModuleConfig(_module_name))

		imported_modules = " ".join(list(self.Modules.keys()))
		logger.info(f"imported: {imported_modules}")
		return list(self.Modules.keys())


	def validate_module_name(self, module_name):
		"""
		If the module is active, and has a cache time set, return "valid"

		:param module_name: The name of the module you want to validate
		:return: The return value is a string.  If the module is valid, the string is "valid".  If the module is not valid, the
		string is "invalid".
		"""

		if module_name not in self.Modules.keys():
			return

		_active = self.Modules[module_name].Settings["active"]
		if _active != "True":
			return

		_cache_time = self.Modules[module_name].Settings["cache_time"]
		if _cache_time == 0:
			return

		return "valid"


	def update_CacheData(self, module_name):
		"""
		The function updates the cache data of a module

		:param module_name: The name of the module
		"""

		_data = self.Modules[module_name].DATA
		_cache_time = self.Modules[module_name].Settings["cache_time"]

		try:
			del_task = "DELETE FROM modules_table WHERE module_name=(%s);"
			self.database.execute_task(del_task, (module_name,))

		except Exception as e:
			logger.error(e)

		try:
			task = "INSERT INTO modules_table(module_name, module_data, module_cache_time) " \
			       "VALUES (%s, %s, %s) " \
			       "ON CONFLICT (module_name) " \
			       "DO UPDATE SET " \
			       "module_data = modules_table.module_data," \
			       "last_update_timestamp = CURRENT_TIMESTAMP"

			self.database.execute_task(task, (module_name, json.dumps(_data), _cache_time))

		except Exception as e:
			logger.error(e)


	@staticmethod
	def validateCache(module_cache_time, last_update_timestamp):
		"""
		If the time since the last update is greater than the cache time, the cache is expired. Otherwise, the cache is valid

		:param module_cache_time: The time in minutes for which the module is cached
		:param last_update_timestamp: The last time the cache was updated
		:return: The status of the cache and the time remaining before it expires.
		"""

		current_time = datetime.datetime.now() - datetime.timedelta(hours=1)
		time_delta = (current_time - last_update_timestamp).total_seconds() // 60
		status = "expired" if time_delta >= module_cache_time else "valid"

		return status, int((module_cache_time - time_delta) * 60)


	@property
	def CacheData(self):
		"""
		This function is used to get the data from the database and return it to the caller
		:return: A dictionary with the module name as the key and a dictionary as the value.
		The value dictionary contains the module cache status, the cache delta, and the module data.
		"""

		query = "SELECT module_name, last_update_timestamp, module_cache_time, module_data FROM modules_table;"
		query_data = self.database.execute_query(query)

		response = {}
		for data in query_data:
			_cache_data = self.validateCache(data[2], data[1])
			response[data[0]] = {"module_cache_status": _cache_data[0],
			                     "cache_delta"        : _cache_data[1],
			                     "module_data"        : data[3]}
		return response
