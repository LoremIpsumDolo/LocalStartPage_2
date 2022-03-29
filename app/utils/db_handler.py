import psycopg2
from rich.console import Console

console = Console()


class Database:
	"""
	database interface
	"""

	def __init__(self, _config):
		self.db_config = _config


	def create_connection(self):
		conn = None

		try:
			params = self.db_config
			conn = psycopg2.connect(**params)

		except Exception as e:
			console.log(e)

		finally:
			return conn


	def test_connection(self):
		conn = self.create_connection()
		try:
			with conn:
				c = conn.cursor()
				c.execute('SELECT version()')
				return f'Postgresql Database version:{c.fetchone()[0]}'

		except Exception as e:
			console.log(e)

		finally:
			if conn is not None:
				conn.close()


	def execute_query(self, query: str, *args):
		conn = self.create_connection()
		try:
			with conn:
				c = conn.cursor()
				if not args:
					c.execute(query)
				else:
					c.execute(query, args)
				return c.fetchall()

		except Exception as e:
			console.log(e)

		finally:
			if conn is not None:
				conn.close()


	def execute_task(self, task: str, *args):
		conn = self.create_connection()
		try:
			with conn:
				c = conn.cursor()
				if not args:
					c.execute(task)

				elif isinstance(args[0], tuple):

					for arg in args:
						c.execute(task, arg)

				elif isinstance(args[0], list):

					for list_item in args:
						for arg in list_item:
							c.execute(task, arg)

		except Exception as e:
			console.log(e)

		finally:
			if conn is not None:
				conn.close()
