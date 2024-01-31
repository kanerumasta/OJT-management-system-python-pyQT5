class Task:
	def __init__(self,title = None,description = None, start = None, due = None,assign_type=None,assign_id = None):
		self._title = title
		self._description = description
		self._start = start
		self._due = due
		self._assign_type = assign_type
		self._assign_id = assign_id
	@property
	def title(self):
		return self._title
	@title.setter
	def title(self,new_title):
		self._title = new_title
	@property
	def description(self):
		return self._description
	@description.setter
	def description(self,desc):
		self._description = desc

	@property
	def start(self):
		return self._start
	@start.setter
	def start(self,start_time):
		self._start = start_time
	@property
	def due(self):
		return self._due
	@due.setter
	def due(self,due):
		self._due = due

	@property
	def assign_type(self):
		return self._assign_type
	@assign_type.setter
	def assign_type(self,assign_type):
		self._assign_type = assign_type

	@property
	def assign_id(self):
		return self._assign_id
	@assign_id.setter
	def assign_id(self,assign_id):
		self._assign_id = assign_id


	

