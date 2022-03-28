# How the Local Startpage works

### What is used:

- the app is based on the python micro-webframework "Flask" and uses a postgresql as database
- in production the app will use gunicorn as wsgi-app and nginx as reverse proxy

***

### General concept:

Flask is used to compose a website from various modules. The content of these modules will be 
either: 
- updated via javascript if fast updates are required (like spotify's "currently playing")
- or be cached in the database and frequently updated, depending on the individual module settings

***

### basic workflow (simplified):

The app is structured in following way:

![](B:\Dokumente\PycharmProjects\LocalStartPage_2\doku\structure.png)


#### initialization:
On startup the app will read the module-configurations stored in module_configs.json.
Each module has a "settings" and a "config" part.

```
  "template"   : {
	"settings": {
	  "module_name"     : "module_template",
	  "module_classname": "ModuleTemplate",
	  "template_name"   : "template.html",
	  "active"          : "False",
	  "cache_time"      : 15
	},
	"config"  : {
	  "remote_server": {
		"url"     : "http://nothing-to-see.xyz/",
		"username": "username",
		"psw"     : "password"
	  }
	}
  }
  ...
```

Every module has the same "settings" fields but can have different "config" fields.
Responsible for managing and interacting with each module is the "module_handler" class.
Depending on the "settings" of each module, the "module_handler" will import and initialize each active module.

**app/__init__.py**

````
from app.modules.module_handler import ModuleHandlerClass
from app.utils.config import config
from app.utils.db_handler import Database

AppConfig = config
database = Database(AppConfig(section='database'))

ModuleHandler = ModuleHandlerClass(database)
ModuleHandler.import_active_Modules()
...
````

**app/modules/module_handler.py**
````
import importlib
import importlib.util
import json
import os


class ModuleHandlerClass:

	def __init__(self, database):
		self.database = database
		self.ConfigFilePath = "app/modules/module_configs.json"
		self.Modules = {}
		
...

	@property
	def Config(self) -> dict:
		with open(self.ConfigFilePath, "r") as file:
			return json.load(file)

	def ModuleConfig(self, module_name):
		return self.Config[module_name]		

...

	def get_active_Modules(self) -> list:

		module_files = [filename.split(".")[0] for filename in os.listdir("app/modules")]

		return [
				module for module in self.Config.keys()
				if self.Config[module]["settings"]["active"] == "True"
				and self.Config[module]["settings"]["module_name"] in module_files
				]


	def import_active_Modules(self) -> None:

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

...				
````


Each module-class will inherent from a "base_module" class which is 
basically a template class and contains code each module requires.

**The base class:**
````
class ModuleTemplate:

	def __init__(self, module_config):
		self.Config = module_config["config"]
		self.Settings = module_config["settings"]
````

**The individual module class:**
````
class ModuleClass(ModuleTemplate):

	def __init__(self, _module_config):
		super().__init__(_module_config)
		
	...	
````


This way every module will be globally accessible via the "module_handler".
To read for example the "config" of the _template_module_:
`ModuleHandler.Modules["template_module"]["Config"]` will be used.
Once the initialization is completed (including the creation of the flask app),
the webserver is ready to server the site itself.

#### serving the website:

