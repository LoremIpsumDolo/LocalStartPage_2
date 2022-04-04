import logging
from app.utils import misc
from app.modules.module_template import ModuleTemplate

logger = logging.getLogger(__name__)


class ModuleClass(ModuleTemplate):

	def __init__(self, _module_config):
		super().__init__(_module_config)
		self.data = []


	@property
	def HostAddress(self) -> str:
		"""
		This function returns the host address of the API
		:return: The host address.
		"""
		return f"{self.Config['host_ip']}:{self.Config['port']}/api/{self.Config['api']}"


	@property
	def DATA(self):
		"""
		The DATA function is called by the Glances class to update the data.
		It calls the fetch_data function to get the data from the server.
		If the fetch_data function returns a value, then the DATA function calls the parse_data function to parse the data.
		If the fetch_data function returns None, then the DATA function returns "unknown"
		:return: The data that is being returned is the data that is being parsed.
		"""
		logger.info("updating glances cache")

		if data := self.fetch_data():
			self.parse_data(data)
			return self.data
		else:
			return "unknown"


	def fetch_data(self) -> dict:
		"""
		This function is used to fetch data from the host address
		:return: A dictionary of dictionaries.
		"""
		try:
			return misc.request_data(url=self.HostAddress, request_type="json")

		except Exception as e:
			logger.error(e)


	def parse_data(self, data: dict) -> None:

		for row in data:
			row_dict = {
					"device_name": row["device_name"],
					"size"       : misc.convert_kb_to_gb(row["size"]),
					"used"       : misc.convert_kb_to_gb(row["used"]),
					"free"       : misc.convert_kb_to_gb(row["free"]),
					"percent"    : row["percent"]
					}
			self.data.append(row_dict)
