from google.appengine.ext import ndb

class Reservation(ndb.Model):
	owner = ndb.StringProperty()
        participants = ndb.StringProperty(repeated=True)
	times_reserveed = ndb.IntegerProperty(repeated=True)
