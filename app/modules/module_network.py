import logging

import requests
from bs4 import BeautifulSoup

from app.modules.module_template import ModuleTemplate

logger = logging.getLogger(__name__)


class ModuleClass(ModuleTemplate):

	def __init__(self, _module_config):
		super().__init__(_module_config)
		self.raw_data = None


	@property
	def DATA(self) -> dict:
		logger.info("updating network cache")

		self.raw_data = self.get_new_data()

		if self.raw_data:
			return {
					'IP'           : self.IP,
					'UPTIME'       : self.UPTIME,
					'ONLINE_STATUS': self.ONLINE_STATUS
					}


	def get_new_data(self):

		try:
			session = requests.Session()
			r = session.get(self.Config["url"])
			soup = BeautifulSoup(r.text, 'html.parser')
			scripts = soup.find_all("script")
			scripts = scripts[9].string.split("\n")
			return [d.strip("var ") for d in scripts[2:-1]]

		except Exception as e:
			logger.error(e)


	@property
	def IP(self):
		return str(self.raw_data[2]).strip("wan_ip=\'").strip("';")


	@property
	def UPTIME(self):
		time_data = str(self.raw_data[1]).split("=")[1].strip("new Array(").strip(")';").split(",")
		return f"{time_data[1]}h : {time_data[2]}m"


	@property
	def ONLINE_STATUS(self):
		if str(self.raw_data[0]).strip("online_status=\'").strip("';") == "1":
			return "online"
		else:
			return "offline"
