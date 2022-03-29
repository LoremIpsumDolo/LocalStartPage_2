import logging
import os

import spotipy

from app.modules.module_template import ModuleTemplate

logger = logging.getLogger(__name__)


class ModuleClass(ModuleTemplate):

	def __init__(self, _module_config):
		super().__init__(_module_config)


	@staticmethod
	def verify_cachedir():
		caches_folder = 'app/.spotify_caches/'

		try:
			if not os.path.exists(caches_folder):
				os.makedirs(caches_folder)

		except Exception as e:
			logger.error(e)


	@property
	def cache_handler(self):
		return spotipy.cache_handler.CacheFileHandler(cache_path='app/.spotify_caches/cache.json')


	@property
	def auth_manager(self):
		return spotipy.oauth2.SpotifyOAuth(
				client_id=self.Config['SPOTIPY_CLIENT_ID'],
				client_secret=self.Config['SPOTIPY_CLIENT_SECRET'],
				redirect_uri=self.Config['SPOTIPY_REDIRECT_URI'],
				scope="user-read-currently-playing",
				show_dialog=True,
				cache_handler=self.cache_handler
				)


	@property
	def SP(self):
		return spotipy.Spotify(auth_manager=self.auth_manager)


	def fetch_data(self) -> dict:

		try:
			return self.SP.current_user_playing_track()

		except Exception as e:
			logger.error(e)


	def parse_data(self) -> dict:

		currently_playing = self.fetch_data()

		if not currently_playing:
			return {"is_playing": False}

		try:
			if not currently_playing["is_playing"]:
				return {"is_playing": currently_playing["is_playing"]}

			else:
				return {"is_playing"   : currently_playing["is_playing"],
				        "timestamp"    : currently_playing["timestamp"],
				        "artist"       : currently_playing["item"]["artists"][0]["name"],
				        "track"        : currently_playing["item"]["name"],
				        "images"       : currently_playing["item"]["album"]["images"][1]["url"],
				        "duration_ms"  : currently_playing["item"]["duration_ms"],
				        "progress_ms"  : currently_playing["progress_ms"],
				        "progress_perc": round(
						        currently_playing["progress_ms"] / currently_playing["item"]["duration_ms"] * 100)
				        }

		except Exception as e:
			logger.error(e)
			return {"is_playing": False}
