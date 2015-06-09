from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound
import requests
import sys
import cherrypy
lib_path = '..'
sys.path.append(lib_path)
import slacker_config

from user_dir_model import User, Base

engine = create_engine('sqlite:///sqlalchemy_users.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
DBSession.bind = engine

# Author: Matt Ankerson
# Date: 28 May 2015

# This is a micro-service intended to recieve and store new users, and validate existing user
# credentials.

class UserDirectory(object):
    exposed = True  # expose all methods
    
    # Add a new user to the db
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        response = {'response': 'success'}  # assume success for now.
        session = DBSession()
        raw_user = cherrypy.request.json  # get the new user
        try:
            new_user = User(id = raw_user['email'], password = raw_user['password'], screen_name = raw_user['screen_name'])
            # we should only add this user if a user with the same email doesn't already exist.
            user_exists = self.GET(new_user.id, new_user.password)
            if user_exists == {'email': 'available', 'password': 'not set'}:
                session.add(new_user)
                session.commit()        # can we get a response from sqlalchemy?
        except IntegrityError, e:
            response['response'] = 'user exists'
        finally:
            session.close()
        return response
        
    # Accept an email and a password
    #   Indicate whether or not the user exists (based on email)
    #   Indicate whether or not the password matches the email
    @cherrypy.tools.json_out()
    def GET(self, email="", password=""):
        response = {'email': 'unavailable', 'password': 'incorrect'}
        # query the sqlite db to find out if this email already exists
        try:
            session = DBSession()
            user_exists = session.query(User).filter(User.id == email).one()
            session.commit()
            if user_exists.password == password:
                response['password'] = 'correct'
            else:
                response['password'] = 'incorrect'
        except MultipleResultsFound, e:
            # in this case, we have a major error
            print(e)
        except NoResultFound, e:
            response = {'email': 'available', 'password': 'not set'}    
        finally:
            session.close()        
        return response
                
        
# switch from the default mechanism of matching URLs to methods
# for one that is aware of the whole HTTP method shenanigan with: MethodDispatcher()
if __name__ == "__main__":
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')],
        }
    }
    
    cherrypy.config.update({'server.socket_port' : slacker_config.urls.port['user_directory']})
    cherrypy.quickstart(UserDirectory(), '/', conf)
        
          