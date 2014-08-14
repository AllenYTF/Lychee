import webapp2
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class DashboardHandler(webapp2.RequestHandler):
    def get(self):
    	template_values = {
            'greetings': "GREETINGS",
            'guestbook_name': "GUESTBOOK NAME",
            'url': "URL",
            'url_linktext': "URL_LINKTEXT",
        }
        template = JINJA_ENVIRONMENT.get_template('dashboard.html')
        self.response.write(template.render(template_values))