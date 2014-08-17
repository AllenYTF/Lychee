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
from google.appengine.api import memcache

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

#Players=[]
#Reservations=[]
#Recent=dict()

memcache.add("player", [], 186400)
memcache.add("reservation", [], 186400)

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
            Players = memcache.get("player")
            print (Players)
            s = "["
            s += ','.join(Players) 
            s += "]"
            self.response.out.write(s)
        except (TypeError, ValueError):
            self.response.out.write("<html><body><p>Invalid inputs</p></body></html>")

class ReservationHandler(webapp2.RequestHandler):
    def get(self):
        try:
            Reservations = memcache.get("reservation")
            s = "["
            s += ','.join(Reservations)
            s += "]"
            self.response.out.write(s)
        except (TypeError, ValueError):
            self.response.out.write("<html><body><p>Invalid data</p></body></html>")

class CreatePlayerHandler(webapp2.RequestHandler):
    def get(self):
        try:
            name = self.request.get("name")
            email = self.request.get("email")
            new_player = '{\"name\": \"%s\", \"email\": \"%s\"}' % (name, email)
            Player = memcache.get("player")
            print "hahah\n\n"
            print Player
            print "heheh\n\n"
            Player.append(new_player)
            print Player
            print "wowow"
           
            print memcache.get("player")
            memcache.set("player", Player, 186400)
            print memcache.get("player")
            memcache.add(name, [], 186400)
        except (TypeError, ValueError):
            self.response.out.write("<html><body><p>Invalid data</p></body></html>")

class CreateReservationHandler(webapp2.RequestHandler):
    def get(self):
        try:
            names = self.request.get("players")
            names_split = names.split(',')
            names_split = ['"'+a+'"' for a in names_split]

#            for name in names_split:
#                for name2 in names_split:
#                    if name is not name2:
#                        if name in Recent:
#                            Recent[name].add(name2)
#                        else:
#                            Recent[name] = set([name2])
            names = ','.join(names_split)
            start = self.request.get("start")
            end = self.request.get("end")
            new_reservation = '{\"players\": [%s], \"start\":\"%s\", \"end\":\"%s\"}' % (names, start, end)
            Reservation = memcache.get("reservation")
            Reservation.append(new_reservation)
            memcache.set("reservation", Reservation, 186400)

            for name in self.request.get("players").split(','):
                Recent = memcache.get(name)
                for other_name in self.request.get("players").split(","):
                    print other_name, name, Recent
                    if other_name != name and other_name not in Recent:
                        Recent += [other_name]
                        print Recent
                memcache.set(name, Recent, 186400)

        except (TypeError, ValueError):
            self.response.out.write("<html><body><p>Invalid data</p></body></html>") 

class GetRecentHandler(webapp2.RequestHandler):
   def get(self):
       try:
            name = self.request.get("name")
            Recent = memcache.get(name)
            names = ['"'+a+'"' for a in Recent]
            s = "["
            s += ','.join(names)
            s += "]"
            self.response.out.write(s)
       except (TypeError, ValueError):
            self.response.out.write("<html><body><p>Invalid data</p></body></html>")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/popup', PopupHandler),
    ('/adduser', AddUserHandler),
    ('/dashboard', DashboardHandler),
    ('/get_public', PublicHandler),
    ('/get_reservations', ReservationHandler),
    ('/create_player', CreatePlayerHandler),
    ('/create_reservation', CreateReservationHandler),
    ('/get_recent', GetRecentHandler)
], debug=True)
