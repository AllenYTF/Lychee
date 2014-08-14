from google.appengine.ext import ndb

class Player(ndb.Model):
    id = ndb.IntegerProperty()
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    games_played = ndb.IntegerProperty()