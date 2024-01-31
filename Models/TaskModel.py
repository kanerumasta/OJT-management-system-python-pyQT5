class Task:
	def __init__(self,title = None,description = None, due = None,created_at = None,status= None):
		self._title = title
		self._description = description
		self._due = due
		self._status = status
		self._created_at = created_at

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
	def due(self):
		return self._due
	@due.setter
	def due(self,due):
		self._due = due

	@property
	def created_at(self):
		return self._created_at

	@created_at.setter
	def created_at(self,date_created):
		self._created_at = date_created

	@property
	def status(self):
		return self._status

	@status.setter
	def status(self,status):
		self._status = status
	
	

