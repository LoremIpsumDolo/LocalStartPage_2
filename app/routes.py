import os
from flask import jsonify, redirect, request, render_template, url_for, send_from_directory, make_response
from app import app, console, ModuleHandler
from rich.pretty import pprint
from functools import wraps
import logging

logger = logging.getLogger(__name__)

Spotify = ModuleHandler.Modules["SpotifyModule"]

# ModuleHandler.update_CacheData("GlancesModule")


@app.route('/')
def url_index():
	return render_template('index.html', Data=ModuleHandler.CacheData)


def make_module_response(_module_name: str, do_update=False):

	if ModuleHandler.validate_module_name(_module_name) != "valid":
		logger.warning(f"{_module_name} module not found")
		return "module not found", 500

	if do_update:
		logger.info(f"updating {_module_name}")
		ModuleHandler.update_CacheData(_module_name)

	template_name = ModuleHandler.Modules[_module_name].Settings["template_name"]

	if template_name not in os.listdir("app/templates/modules"):
		logger.warning("template not found")
		return "template not found", 500

	template_file = f"modules/{template_name}"

	return make_response(render_template(template_file, Data=ModuleHandler.CacheData))


def validate_module_request(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):

		if not request.args.get("module_name"):
			logger.warning("missing module_name")
			return "missing module_name", 500

		return f(*args, **kwargs)

	return decorated_function


@app.route('/module')
@validate_module_request
# /module?module_name=NetworkModule
def url_module_by_name():

	module_name = request.args.get("module_name")
	return make_module_response(module_name)


@app.route('/update_module')
@validate_module_request
# /update_module?module_name=NetworkModule
def url_update_module_by_name():

	module_name = request.args.get("module_name")
	return make_module_response(module_name, True)

#################
#   MODULES    #
###############


@app.route('/spotify')
def spotify():

	if not Spotify.auth_manager.validate_token(Spotify.cache_handler.get_cached_token()):
		auth_url = Spotify.auth_manager.get_authorize_url()
		return f'<h2><a href="{auth_url}">Sign in</a></h2>'

	if data := Spotify.parse_data():
		return render_template('modules/spotify.html', data=data)
	else:
		return "", 200


@app.route('/spotify/callback/')
def spotify_callback():

	if request.args.get("code"):
		Spotify.auth_manager.get_access_token(request.args.get("code"))

	return redirect('/')


# weather

@app.route('/weather_widget')
def url_weather_widget():
	api_key = ModuleHandler.Modules["WeatherModule"].Config['apikey']
	return render_template('modules/weather_widget.html', api_key=api_key)


##################
#   SETTINGS    #
################


@app.route('/settings')
def url_settings():
	return render_template('settings.html', Data=ModuleHandler)


@app.route('/settings/edit', methods=['POST', 'GET'])
def url_settings_edit():
	pprint(request.args.get)
	return "", 200
	# return render_template('settings.html', Data=ModuleHandler)