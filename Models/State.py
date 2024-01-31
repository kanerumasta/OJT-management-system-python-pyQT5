class State:
	def __init__(self,data = None):
		self._data = data

	@property
	def data(self):
		return self._data

	@data.setter
	def data(self,data):
		self._data = data

	
	