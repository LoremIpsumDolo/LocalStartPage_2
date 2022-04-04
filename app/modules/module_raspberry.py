import logging

import xmltodict

from app.modules.module_template import ModuleTemplate
from app.utils import misc

logger = logging.getLogger(__name__)


class ModuleClass(ModuleTemplate):

	def __init__(self, _module_config):
		super().__init__(_module_config)
		self.data = []


	@property
	def DATA(self):
		"""
		The DATA function is called by the Glances class to update the data.
		It calls the fetch_data function to get the data from the server.
		If the fetch_data function returns a value, then the DATA function calls the parse_data function to parse the data.
		If the fetch_data function returns None, then the DATA function returns "unknown"
		:return: The data that is being returned is the data that is being parsed.
		"""
		logger.info("updating raspberry cache")

		if data := self.fetch_data():
			self.parseXML(data)
			return self.data
		else:
			return "unknown"


	def fetch_data(self):
		url = f"{self.Config['hostname']}_status?format=xml"
		username = self.Config['username']
		psw = self.Config['psw']

		return misc.request_data(url=url, request_type="xml", username=username, psw=psw)


	def parseXML(self, rawXML):
		raw_dict = xmltodict.parse(str(rawXML))
		raw_dict = raw_dict['html']['body']['monit']

		host_data = {
				"hostname": raw_dict["server"]["localhostname"],
				"services": self.get_services(raw_dict),
				"storage" : self.get_storage(raw_dict)
				}

		self.data.append(host_data)


	def get_services(self, xml_data) -> list:

		service_data_collection = []

		for data in xml_data["service"]:

			if data["@type"] == "3":

				service_data = {
						"status"      : None,
						"uptime"      : 0,
						"memory"      : 0,
						"cpu"         : 0,
						"service_name": data["name"],
						}

				if data["monitor"] != "1":
					service_data["status"] = "not monitored"
				else:
					service_data["status"] = "monitored"
					service_data["uptime"] = misc.seconds_to_day_time_str(data["uptime"])
					service_data["memory"] = data["memory"]["percenttotal"]
					service_data["cpu"] = data["cpu"]["percent"]

				service_data_collection.append(service_data)

		return service_data_collection


	def get_storage(self, xml_data) -> list:

		def prep_int(data: str) -> int:
			x = data.split(".")[0]
			return int(x)


		storage_data_collection = []

		for data in xml_data["service"]:

			if data["@type"] == "0":

				total = prep_int(data["block"]["total"])
				used = prep_int(data["block"]["usage"])
				free = total - used

				storage_data = {
						"name"   : data["name"],
						"percent": int(round(float(data["block"]["percent"]))),
						"free"   : misc.convert_mb_to_gb(free),
						"total"  : misc.convert_mb_to_gb(total),
						}

				storage_data_collection.append(storage_data)

		return storage_data_collection
