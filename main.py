from google.appengine.ext import ndb
import os
import MySQLdb
import webapp2
import json

# These environment variables are configured in app.yaml.
CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')


def connect_to_cloudsql():
    # When deployed to App Engine, the `SERVER_SOFTWARE` environment variable
    # will be set to 'Google App Engine/version'.
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        # Connect using the unix socket located at
        # /cloudsql/cloudsql-connection-name.
        cloudsql_unix_socket = os.path.join(
            '/cloudsql', CLOUDSQL_CONNECTION_NAME)

        db = MySQLdb.connect(
            unix_socket=cloudsql_unix_socket,
            user=CLOUDSQL_USER,
            passwd=CLOUDSQL_PASSWORD)

    # If the unix socket is unavailable, then try to connect using TCP. This
    # will work if you're running a local MySQL server or using the Cloud SQL
    # proxy, for example:
    #
    #   $ cloud_sql_proxy -instances=your-connection-name=tcp:3306
    #
    else:
        db = MySQLdb.connect(
            host='127.0.0.1', user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD)

    return db


class Message(ndb.Model):
    """Message model"""
    sender = ndb.StringProperty()
    recipient = ndb.StringProperty()
    msg = ndb.TextProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):
    """
    This class takes care of the main page on a web interface. 
    """
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('CMPS 121 - webapp2 testing server')

     db = connect_to_cloudsql()
     #cursor = db.cursor()
     #cursor.execute('SHOW VARIABLES')

##     for r in cursor.fetchall():
##         def get(self):
##            self.response.headers['Content-Type'] = 'application/json'
##            self.response.write(json.dumps(dict(cat=4, dog=4, bird=2, spider=8)))
##            self.response.write('{}\n'.format(r))

class GetListPage(webapp2.RequestHandler):
    """
    This class defines the call to get a fixed list
    """
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(dict(cat=4, dog=4, bird=2, spider=8)))


class SendMsgPage(webapp2.RequestHandler):
    """
    This class provides a GET call used to store message information in Datastore.
    Uses NDB.
    """
    def get(self):
        sender = self.request.get('sender')
        recipient = self.request.get('recipient')
        msg = self.request.get('message')

        # NDB interaction
        msg_entry = Message(sender=sender, recipient = recipient, msg=msg)
        msg_entry.put()

        self.response.write("ok")



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/get_list', GetListPage),
    ('/send_msg', SendMsgPage),
], debug=True)
