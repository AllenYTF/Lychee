from google.appengine.ext import ndb

class Reservation(ndb.Model):
	id = ndb.IntegerProperty()
	playerId = ndb.IntegerProperty(repeated=True)
	times_reserveed = ndb.IntegerProperty(repeated=True)