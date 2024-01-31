
class Trainee:
	def __init__(self,id=None,firstname=None,lastname=None,email=None,course=None,contact=None,school_id=None):
		self._id = id
		self._firstname = firstname
		self._lastname = lastname
		self._email = email
		self._course = course
		self._contact = contact
		self._school_id = school_id

	@property
	def id(self):
		return self._id

	@id.setter
	def id(self,id):
		self._id=id

	@property
	def firstname(self):
		return self._firstname
	
	@firstname.setter
	def firstname(self,firstname):
		self._firstname = firstname

	@property
	def lastname(self):
		return self._lastname
	@lastname.setter
	def lastname(self,lastname):
		self._lastname = lastname
	@property
	def email(self):
		return self._email
	@email.setter
	def email(self,email):
		self._email = email

	@property
	def course(self):
		return self._course
	@course.setter
	def course(self,course):
		self._course = course
	@property
	def school_id(self):
		return self._school_id
	@school_id.setter
	def school_id(self,school_id):
		self._school_id = school_id
	@property
	def contact(self):
		return self._contact
	@contact.setter
	def contact(self,contact):
		self._contact = contact
	

