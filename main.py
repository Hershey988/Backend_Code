#from google.appengine.ext import ndb
#from bs4 import BeautifulSoup
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


##class Message(ndb.Model):
##    """Message model"""
##    sender = ndb.StringProperty()
##    recipient = ndb.StringProperty()
##    msg = ndb.TextProperty()
##    date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):
    """
    This class takes care of the main page on a web interface. 
    """
    def get(self):
        #soup = BeautifulSoup(page.content, 'html.parser')
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('CMPS 121 - webapp2 testing server')

        db = connect_to_cloudsql()
        cursor = db.cursor()
        cursor.execute('SHOW VARIABLES')
        #word = ""
        #for r in cursor.fetchall():
            #def get(self):
            #print r[0]
             #word = '{} {}'.format(r)

        #self.response.headers['Content-Type'] = 'text/plain'
        #self.response.write(json.dump(cursor.fetchall()))
        

class GetListPage(webapp2.RequestHandler):
    """
    This class defines the call to get a fixed list
    """
    
    def get(self):
        w = 'hi'
        x = 'hello'
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(dict(name=w, idd=x, cat=4, dog=4, bird=2, spider=8)))


class LogInPage(webapp2.RequestHandler):
    def get(self):
        userID = self.request.get('userID', default_value='')

        db = connect_to_cloudsql()
        cursor = db.cursor()
        namedb = "USE Wheysted;"
        cursor.execute(namedb)

        check = "SELECT userID FROM Wheysted.user WHERE userID LIKE ('%s');" % (userID)
        query = cursor.execute(check)
        if query != 1:
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps(dict(code="ADD")))
        else    
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps(dict(code="EXIST")))


class New_Login(webapp2.RequestHandler):
    """Login page class, for new user to sign-in with Google and register."""

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Create a new account!')
        #GET from databse to confirm contents
        db = connect_to_cloudsql()
        cursor = db.cursor()
        cursor.execute('SHOW VARIABLES')

class AddUserPage(webapp2.RequestHandler):       
    def post(self):
        fName = self.request.get('fname', default_value='')
        lname = self.request.get('lname', default_value='')
        userID = self.request.get('userID', default_value='')

        #Either add to the DB or Delete from it
        if ADD:
            addUser()
        else:
            delUser()

        #db = connect_to_cloudsql()
        #cursor = db.cursor()
        #cursor.execute()

    def addUser(): #Add the new user information to Database
        db = connect_to_cloudsql()
        x = db.cursor()

        try:
            x.execute("INSERT INTO user(userID, profileID) values ('%s', '%d');" % ("Hari", 1))
            db.commit()
        except:
            db.rollback()
        db.close()

    def delUser(): #Remove existing user information from Database
        db = connect_to_cloudsql()
        x = db.cursor()

        try:
            x.execute("DELETE FROM user where userID = ('%s');" % ("Hari"))
            db.commit()
        except:
            db.rollback()
        db.close()

        #HANDLE: ACCOUNT ALREADY EXISTS!!!
        #METHOD TO GO TO MAIN PAGE AFTER SUCCESSFUL LOGIN


class Existing_Login(webapp2.RequestHandler):
    """Login page class, for returning user to sign-in with Google"""

    #GET method, should GET existing account from Database
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Retrieving account...')
        #GET from databse to confirm contents
        db = connect_to_cloudsql()
        cursor = db.cursor()
        cursor.execute('SHOW VARIABLES')

        try:
            check = "SELECT userID FROM Wheysted.user WHERE userID LIKE ('%s');" % (userID) query = x.execute(check)
        if query != 1:
            self.response.headers["Content-Type"] = 'application/json'
            self.response.write('Error, account not found')
            self.response.write(json.dumps(dict(code="FAILURE")))
            #METHOD TO GO TO NEW_LOGIN PAGE
        else:
            self.response.headers["Content-Type"] = 'application/json'
            self.response.write('logging in...')
            self.response.write(json.dumps(dict(code="SUCCESS")))
            #LOGIN

class AddUserPage(webapp2.RequestHandler):       
    def post(self):
        fName = self.request.get('fname', default_value='')
        lname = self.request.get('lname', default_value='')
        userID = self.request.get('userID', default_value='')

        
        db = connect_to_cloudsql()
        cursor = db.cursor()
        namedb = "USE Wheysted;"
        cursor.execute(namedb)
        # Prepare SQL query to INSERT a record into the database.
        if fname != '' and lname != '' and userID != '':
            sql = "INSERT INTO user(userID) values ('%s');" % (userID)
            try:
               # Execute the SQL command
               cursor.execute(sql)
               # Commit your changes in the database
               db.commit()
               self.response.write("SUCCESSFUL: Done adding")
            except:
               # Rollback in case there is any error
               self.response.write("THERE WAS AN ERROR: rolling back")
               db.rollback()
               
                 
               #self.response.write("ok")
               db.close()
        else:
            self.response.write("600: USER or ID is not defines")


class ProfilePage(webapp2.RequestHandler):
    def post(self):
        sender = self.request.get('sender', default_value='')
        recipient = self.request.get('recipient', default_value='')
        msg = self.request.get('message', default_value='')

        """if ADD:
            addSpec()
        else if DELETE:
            delSpec()
        else:
            if string input:
                modSpecString()
            if int input:
                modSpecInt():
            else:
                return error"""

        
        #db = connect_to_cloudsql()
        #x = db.cursor()

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Showing changes...')
        #GET from databse to confirm contents
        db = connect_to_cloudsql()
        cursor = db.cursor()
        cursor.execute('SHOW VARIABLES')

    #Add an entire set of user specifications
    def addSpec():
        db = connect_to_cloudsql(): #first, connect to the cloud database
        x = db.cursor()
        try: 
            x.execute("INSERT INTO Profile VALUES (%s, %s, %d, %d, %s, %s);" % ("Hari", "Dasarathy", 20, 180, "High", "180"))
            db.commit()
        except:
            db.rollback()
        db.close()

    #delete an entire set of user specifications
    def delSpec():
        db = connect_to_cloudsql()
        x = db.cursor()

        try:
            check = "SELECT userID FROM Wheysted.user WHERE userID LIKE ('%s');" % (userID) query = x.execute(check)
            if query != 1: 
                self.response.headers["Content-Type"] = 'application/json'
                self.response.write(json.dumps(dict(code="N/A")))
            else:
                self.response.headers["Content-Type"] = 'application/json'
                self.response.write(json.dumps(dict(code="DEL")))


            x.execute("DELETE FROM Profile where profileID = ('%d');" % ("Hari"))
            db.commit()
        except:
            db.rollback()
        db.close()

    #modify one user specification
    def modSpecString():
        db = connect_to_cloudsql()
        x = db.cursor()

        try:
            check = "UPDATE profile SET ('%s') = ('%s') WHERE profileID = ('%d');" % (column_name, user_string, profileID) query = x.execute(check)
            if query != 1:
                self.response.headers["Content-Type"] = 'application/json'
                self.response.write(json.dumps(dict(code="FAILURE")))
            else:
                self.response.headers["Content-Type"] = 'application/json'
                self.response.write(json.dumps(dict(code="UPDATED")))

            db.commit()
        except:
            db.rollback()
        db.close()

    def modSpecInt():
        db = connect_to_cloudsql()
        x = db.cursor()

        try:
            check = "UPDATE profile SET ('%s') = ('%d') WHERE profileID = ('%d');" % (column_name, user_int, profileID) query = x.execute(check)
            if query != 1:
                self.response.headers["Content-Type"] = 'application/json'
                self.response.write(json.dumps(dict(code="FAILURE")))
            else:
                self.response.headers["Content-Type"] = 'application/json'
                self.response.write(json.dumps(dict(code="UPDATED")))

            db.commit()
        except:
            db.rollback()
        db.close()       

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/get_list', GetListPage),
    ('/login', LoginPage),
    ('/adduser', AddUserPage),
], debug=True)
