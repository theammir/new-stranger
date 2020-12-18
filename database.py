import tinydb

class Instance:
	def __init__(self, path):
		self.db = tinydb.TinyDB(path)
		self.query = tinydb.Query()


	def add_item(self, item):
		self.db.insert(item)

	def find_item(self, **kwargs):
		for k, v in kwargs.items():
			items = self.db.search(self.query[k] == v)
		if (items):
			return items[0]
		else:
			return items

	def find_items(self, table, condition):
		for k, v in kwargs.items():
			items = self.db.search(self.query[k] == v)
			return items
