import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from flask import Flask
from flask_cors import CORS
from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install

from app.modules.module_handler import ModuleHandlerClass
from app.utils.config import config
from app.utils.db_handler import Database

# from flask.logging import default_handler

app = Flask(__name__)
app.config['SECRET_KEY'] = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
cors = CORS(app)
# app.logger.removeHandler(default_handler)

AppConfig = config
database = Database(AppConfig(section='database'))

ModuleHandler = ModuleHandlerClass(database)
ModuleHandler.import_active_Modules()


def make_logger():
	"""
	Create a logger that logs to a file and to the console
	"""
	install(show_locals=True)
	path = "app/logs/server.log"
	Path('app/logs/').mkdir(parents=True, exist_ok=True)

	logger = logging.getLogger(__name__)
	debug_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
	file_handler = RotatingFileHandler(path,
	                                   maxBytes=1000000,
	                                   backupCount=10)

	file_handler.setFormatter(debug_formatter)
	logger.setLevel(logging.DEBUG)
	logger.addHandler(file_handler)
	logger.addHandler(RichHandler(rich_tracebacks=True))

	werkzeug_logger = logging.getLogger('werkzeug')
	werkzeug_logger.setLevel(logging.INFO)
	# werkzeug_handler = logging.StreamHandler()
	# werkzeug_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
	# werkzeug_handler.setFormatter(werkzeug_formatter)
	# werkzeug_logger.addHandler(werkzeug_handler)
	# werkzeug_logger.addHandler(RichHandler(rich_tracebacks=True))

	# root = logging.getLogger()
	# root.addHandler(RichHandler(rich_tracebacks=True))


make_logger()
console = Console()
