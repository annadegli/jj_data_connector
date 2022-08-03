import sqlite3
from sqlite3 import Error

"""
Rename module to connectordb
"""

class ConnectorDBException(Exception):
	"""Connector Exception Base class"""

class ConnectorConnectionAbsent(ConnectorDBException):
	""""""

class ItemAlreadyExists(ConnectorDBException):
	""""""

class TableInvalid(ConnectorDBException):
	""""""

def create_tables(table_name):
	if table_name == 'GA4':
		sql = '''
			CREATE TABLE IF NOT EXISTS GA4_Queries (
				Query_Name TEXT NOT NULL PRIMARY KEY,
				Dimensions TEXT,
				Metrics TEXT,
				Start_Date TEXT,
				End_Date TEXT,
				Note TEXT,
				Row_Limit INT,
				Row_Offset INT,
				Created TEXT DEFAULT CURRENT_TIMESTAMP
			);
		'''
		return sql
	elif table_name == 'GSC':
		sql = '''
			CREATE TABLE IF NOT EXISTS GSC_Queries (
				Query_Name TEXT NOT NULL PRIMARY KEY,
				Dimensions TEXT,				
				Start_Date TEXT,
				End_Date TEXT,
				Note TEXT,
				Created TEXT DEFAULT CURRENT_DATE
			);			
		'''
		return sql
	else:
		raise TableInvalid("Invalid Table Item")


class ConnectorQueryDB:
	def __init__(self, db_file=None):
		self.db_file = db_file
		self.conn = None
		
	def create_connection(self):
		if self.db_file is None:
			self.conn = sqlite3.connect(':memory:')
		else:
			try:
				self.conn = sqlite3.connect(self.db_file)
				return True
			except Exception as e:
				print(e)

	def create_data_models(self):
		# if self.conn is None:
		# 	raise ConnectorConnectionAbsent("Connection is absent")
		self.create_connection()
		cursor = self.conn.cursor()
		cursor.execute(create_tables('GA4'))
		cursor.execute(create_tables('GSC'))
		self.conn.commit()
		self.terminate_connection()

	def insert_ga4_queries(self, query_name, dimensions, metrics, start_date, end_date, note, row_limit, row_offset):
		try:
			self.create_connection()
			cur = self.conn.cursor()
			cur.execute("""
				INSERT INTO GA4_Queries (Query_Name, Dimensions, Metrics, Start_Date, End_Date, Note, Row_Limit, Row_Offset)
				VALUES
				(?, ?, ?, ?, ?, ?, ? , ?)
			""", (query_name, dimensions, metrics, start_date, end_date, note, row_limit, row_offset))

			self.conn.commit()
			self.terminate_connection()
		except Exception as e:
			raise ConnectorDBException(e)

	def queryUpdate(self, sql, update_items=None):
		self.create_connection()
		cursor = self.conn.cursor()
		cursor.execute(sql, update_items)
		self.conn.commit()
		self.terminate_connection()


	def queryRows(self, sql):
		self.create_connection()
		cursor = self.conn.cursor()
		cursor.execute(sql)
		records = cursor.fetchall()
		return records
		self.terminate_connection()

	def terminate_connection(self):
		if self.conn:
			self.conn.close()

	def _exception_test(self):
		if self.conn is None:
			try:
				raise ConnectorConnectionAbsent("Connection is absent")

			except ConnectorConnectionAbsent as e:
				print('x')
				print(e)
			else:
				print('x')

		
if __name__ == "__main__":
	slite = ConnectorQueryDB('connector.db')
	slite.create_connection()
	# slite._exception_test()
	slite.create_data_models()

	# cur = slite.conn.cursor()
	# r = cur.execute("""
	# 	SELECT * FROM GA4_Queries
	# """)
	# print(r.fetchall())
	# slite.terminate_connection()

	# cur.execute("DROP TABLE GA4_Queries")
	# slite.conn.commit()

	# print(create_tables('GA4'))