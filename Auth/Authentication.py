import cherrypy
import json
import uuid
import sys
lib_path = '..'
sys.path.append(lib_path)
from slacker_config import urls

class AuthService():
    exposed = True

    def __init__(self):
        #list of sessions
        self.sessions = {}

    def add_session(self, username):
        #add session
        self.sessions[uuid.uuid4()] = {'user_id' : username}

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def remove_session(self, username):
        username = cherrypy.request.json
        #delete session from list
        if username in self.sessions:
            self.sessions.remove(self.sessions.index(username))
            return True
        else:
            return False

    # Takes request from login
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def validator(self):
        request_data = cherrypy.request.json
        username = request_data['username']
        password = request_data['password']

        #takes username and password
        #sends it to the db
        self.is_present = self.check_user_db(username, password)
        if(self.is_present):
            #give them a session
            # Ask DB people how to check
            self.add_session(username)
            return {'valid': True }
        else:
            # return error
            return {'valid': False, 'message': 'Not in database' }


    # Checks if the user is in the user DB
    def check_user_db(self, username, password):
        self.checked = False
        #check the db if present
        return self.checked

    # Checks if the user has a current session running, returns true or false
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        key = cherrypy.request.json
        #check if the current session is in use
        if key['session_key'] in self.sessions:
            return {'user_id': 'steve'} # Check with message writers about response format
        else:
            return {'test': 'json'}



if __name__ == "__main__":
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }
    cherrypy.config.update({'server.socket_port': urls.port['auth']})
    cherrypy.quickstart(AuthService(), '/', conf)