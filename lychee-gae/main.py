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
from model_players import Player
from model_reservations import Reservation
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())

class CalendarHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('The current time is ' + str(time.localtime()) + '!')

class PopupHandler(webapp2.RequestHandler):
    def get(self):
        players = Player.query()
        self.response.write("listing all players in the db:")
        for player in players:
            self.response.write(player.name)

class AddUserHandler(webapp2.RequestHandler):
    def get(self):
        player = Player(id=1, name="test_user", email="test@adap.tv", games_played=99)
        player.put()

class PublicHandler(webapp2.RequestHandler):
    def get(self):
        try:
            with open("data/player.json") as player:
                self.response.out.write(player.read())
        except (TypeError, ValueError):
            self.response.out.write("<html><body><p>Invalid inputs</p></body></html>")

class ReservationHandler(webapp2.RequestHandler):
    def get(self):
        try:
            with open("data/reservation.json") as reservation:
                self.response.out.write(reservation.read())
        except (TypeError, ValueError):
            self.response.out.write("<html><body><p>Invalid data</p></body></html>")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/popup', PopupHandler),
    ('/adduser', AddUserHandler),
    ('/dashboard', DashboardHandler),
    ('/get_public', PublicHandler),
    ('/get_reservations', ReservationHandler)
], debug=True)
