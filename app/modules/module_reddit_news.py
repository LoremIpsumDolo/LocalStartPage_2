import logging

from app.modules.module_template import ModuleTemplate
from app.utils import misc

logger = logging.getLogger(__name__)


class ModuleClass(ModuleTemplate):

	def __init__(self, _module_config):
		super().__init__(_module_config)
		self.data = []


	@property
	def sources(self):
		return self.Config["urls"]


	@property
	def DATA(self):

		try:
			for source in self.sources:

				if data := self.fetch_data(source):
					self.parse_data(data, source)

			return self.data

		except Exception as e:
			logger.error(e)


	@staticmethod
	def fetch_data(source: str):

		logger.info(f"fetching reddit-news-data for {source}")
		url = f"https://en.reddit.com/r/{source}/new.json"

		try:
			return misc.request_data(url=url, request_type="json")

		except Exception as e:
			logger.error(e)


	def parse_data(self, data, source: str):

		source_dict = {"source_name": source,
		               "source_data": []}

		for post in data["data"]["children"]:
			row_dict = {
					"title"      : post["data"]["title"],
					"url"        : post["data"]["url"],
					"domain"     : post["data"]["domain"],
					"permalink"  : post["data"]["permalink"],
					"created_utc": misc.convert_timestamp(post["data"]["created_utc"])
					}
			source_dict["source_data"].append(row_dict)

		self.data.append(source_dict)
