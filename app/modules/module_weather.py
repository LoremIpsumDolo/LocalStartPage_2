import logging

from app.modules.module_template import ModuleTemplate
from app.utils import misc

logger = logging.getLogger(__name__)


class ModuleClass(ModuleTemplate):

	def __init__(self, _module_config):
		super().__init__(_module_config)
		self.icon_url = "https://openweathermap.org/img/wn/"


	@property
	def DATA(self) -> dict:
		logger.info("updating weather cache")

		if raw_data := self.fetch_data():
			return self.parse_data(raw_data)


	def fetch_data(self):
		ApiKey = self.Config["apikey"]
		one_call_url = f"https://api.openweathermap.org/data/2.5/onecall?lat=52.52&lon=13.41&exclude=hourly,minutely,alerts&appid={ApiKey}&units=metric"

		# if response := misc.request_json(one_call_url):
		# 	misc.save_json("app/modules/weather.json", response)
		# 	return response

		return misc.open_json("app/modules/weather.json")

	def parse_data(self, raw_data):
		try:
			return {
					"current"     : int(raw_data["current"]["temp"]),
					"icon"        : f'{self.icon_url}{raw_data["current"]["weather"][0]["icon"]}.png',
					"future_day"  : int(raw_data["daily"][0]["temp"]["day"]),
					"future_night": int(raw_data["daily"][0]["temp"]["night"]),
					}
		except Exception as e:
			logger.error(e)
