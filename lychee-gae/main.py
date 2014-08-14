#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import calendar
import time
from dashboard import DashboardHandler

timeBuckets = []
for i in range(0,288):
	timeBuckets.append(False);

from google.appengine.ext import ndb

class Reservation(ndb.Model):
	id = ndb.IntegerProperty()
	playerId = ndb.IntegerProperty(repeated=True)
	times_reserveed = ndb.IntegerProperty(repeated=True)

class Player(ndb.Model):
    id = ndb.IntegerProperty()
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    games_played = ndb.IntegerProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('This is Lychee!')

class CalendarHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('The current time is ' + str(time.localtime()) + '!')

class PopupHandler(webapp2.RequestHandler):
    def get(self):
        players = Player.query()
        for player in players:
            self.response.write(player)

class AddUserHandler(webapp2.RequestHandler):
    def get(self):
        player = Player(id=1, name="test_user", email="test@adap.tv", games_played=99)
        player.put()

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/popup', PopupHandler),
    ('/adduser', AddUserHandler),
    ('/dashboard', DashboardHandler)
], debug=True)
