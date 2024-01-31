class School:
    def __init__(self, sid=None, name=None, address=None, coordinator=None, contact=None, requiredHours=None, initials=None):
        self._sid = sid
        self._name = name
        self._address = address
        self._coordinator = coordinator
        self._contact = contact
        self._requiredHours = requiredHours
        self._initials = initials

    @property
    def sid(self):
        return self._sid

    @sid.setter
    def sid(self, sid):
        self._sid = sid

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address

    @property
    def coordinator(self):
        return self._coordinator

    @coordinator.setter
    def coordinator(self, coordinator):
        self._coordinator = coordinator

    @property
    def contact(self):
        return self._contact

    @contact.setter
    def contact(self, contact):
        self._contact = contact

    @property
    def requiredHours(self):
        return self._requiredHours

    @requiredHours.setter
    def requiredHours(self, requiredHours):
        self._requiredHours = requiredHours

    @property
    def initials(self):
        return self._initials

    @initials.setter
    def initials(self,initials):
        self._initials = initials
