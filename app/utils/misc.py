import json
import time
from datetime import datetime, timedelta

import requests
from requests.exceptions import ConnectionError
import requests_random_user_agent
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from rich.console import Console

console = Console()


def j_print(data: str):
	print(json.dumps(data, indent=4))


def open_json(_path: str):
	content = None
	try:
		with open(_path, "r") as f:
			content = json.load(f)

	except Exception as e:
		console.log(e)

	finally:
		return content


def save_json(_filename, content):
	try:
		with open(_filename, "w") as f:
			f.write(json.dumps(content, indent=4, ensure_ascii=True))

	except Exception as e:
		console.log(e)


def request_json(url, username=None, psw=None):
	try:
		session = requests.Session()
		if username or psw:
			r = session.get(url, auth=(username, psw))
		else:
			r = session.get(url)
		return r.json()

	except Exception as e:
		console.log(e)


def request_url(url):
	try:
		session = requests.Session()
		r = session.get(url)
		return BeautifulSoup(r.text, 'html.parser')

	except Exception as e:
		console.log(e)


def fetch_raw_xml(url: str, username: str, psw: str):
	try:
		r = requests.get(url, auth=(username, psw))
		return BeautifulSoup(r.content, "lxml")

	except Exception as e:
		console.log(e)


def request_data(url: str, request_type=None, username=None, psw=None):
	adapter = HTTPAdapter(max_retries=3)
	session = requests.Session()
	session.mount('https://', adapter)
	session.mount('http://', adapter)

	try:
		if username and psw:
			r = session.get(url, auth=(username, psw), timeout=(10, 10))
		else:
			r = session.get(url, timeout=(10, 10))

		if request_type == "xml":
			return BeautifulSoup(r.content, "lxml")

		elif request_type == "json":
			return r.json()

		else:
			return BeautifulSoup(r.text, 'html.parser')

	except Exception as e:
		console.log(e)


def convert_kb_to_mb(_kb: int) -> int:
	return round(_kb / 1024)


def convert_mb_to_gb(_mb: int) -> float:
	return round(_mb / 1024, 1)


def convert_kb_to_gb(_kb: int) -> int:
	_gb = _kb
	for _ in range(3):
		_gb = round(_gb / 1024)

	return _gb


def GetHumanReadable(size, precision=2):
	suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
	suffixIndex = 0
	while size > 1024 and suffixIndex < 4:
		suffixIndex += 1  # increment the index of the suffix
		size = size / 1024.0  # apply the division
	return "%.*f%s" % (precision, size, suffixes[suffixIndex])


def convert_timestamp(t):
	current_time = datetime.fromtimestamp(int(time.time())) - timedelta(hours=1)
	post_time = datetime.fromtimestamp(int(t))
	time_delta_seconds = (current_time - post_time).total_seconds()
	time_delta_str = None

	if time_delta_seconds < 60:
		time_delta_str = f"{int(time_delta_seconds)} seconds ago"

	else:
		time_delta_minutes = time_delta_seconds // 60
		if time_delta_minutes < 60:
			time_delta_str = f"{int(time_delta_minutes)} minutes ago"

		else:
			time_delta_hours = time_delta_minutes // 60
			if time_delta_hours < 24:
				time_delta_str = f"{int(time_delta_hours)} hours ago"

			else:
				time_delta_days = time_delta_hours // 24
				time_delta_str = f"{int(time_delta_days)} day(s) ago"

	return time_delta_str


def seconds_to_day_time_str(sec) -> str:
	seconds = int(sec)
	minutes = seconds // 60
	hours = minutes // 60
	days = hours // 24
	return f"{days}d {hours % 60}h {minutes % 60}m"
	# print("%02d:%02d:%02d:%02d" % (days, hours % 24, minutes % 60, seconds % 60))
