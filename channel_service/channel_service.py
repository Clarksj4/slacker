__author__ = 'alexmcneill'
import sys
import cherrypy
import requests
from channel_service_dicts import add_channel_response, delete_channel_response, read_channel_response
from pymongo import MongoClient
lib_path = '..'
sys.path.append(lib_path)
import slacker_config


class Root:
    exposed = True

    def index(self):
        return "Go to /channels to start using the channels webservice"

# Class for managing all channel requests
class ChannelWebService:
    exposed = True

    def __init__(self):
        client = MongoClient()
        self.channel_db = client["channel_db"]
        self.channel_collection = self.channel_db.channels

    @cherrypy.tools.json_out()
    def GET(self, channel_id= None):

        try:
            # Making sure the channel id passed in was an int
            channel_id = int(channel_id)

            # Fetching the channel
            channel_json = self.channel_collection.find_one({"_id": channel_id})

            # Checking that there was a channel found and returning the result
            if channel_json is None:
                return read_channel_response("No matching channel", 1)
            else:
                return read_channel_response("Channel found", 0, channel_json)

        except ValueError:
            return read_channel_response("Invalid input", 1)
        except:
            return read_channel_response("Unable to connect to database", 1)

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):

        try:
            # Getting the json input
            new_channel_request = cherrypy.request.json

            # Checking if a channel already exists by the input name
            channel_json = self.channel_collection.find_one({"name": new_channel_request["name"]})

            if channel_json is not None:
                return add_channel_response("There is already a channel by that name", 1)
            else:
                # Getting a id for the new channel
                latest_channel_json = self.channel_collection.find_one({"$query": {}, "$orderby": {"_id": -1}})
                new_channel_id = 1

                if latest_channel_json is not None:
                    new_channel_id = latest_channel_json["_id"] + 1

                # Creating a dict that the database will accept for a new channel input
                new_channel_json = {"_id": new_channel_id, "name": new_channel_request["name"], "owner": new_channel_request["owner"]}

                # Adding the channel to the database
                self.channel_collection.insert_one(new_channel_json)

                return add_channel_response("Channel added", 0)
        except KeyError:
            return add_channel_response("Invalid channel request", 1)
        except:
            return add_channel_response("Unable to connect to database", 1)

    @cherrypy.tools.json_out()
    def DELETE(self, channel_id):
        try:
            # Making use the input id is an int
            channel_id = int(channel_id)

            # Deleting channel
            delete_result = self.channel_collection.delete_one({"_id": channel_id})

            # Checking that a channel was deleted
            if delete_result > 0:
                # Requesting that the message service delete all messages associated with the channel
                host = slacker_config.urls.url["messages"]
                host_port = slacker_config.urls.port["messages"]

                r = requests.get("{0}:{1}/?channel_id={2}&message_id=all".format(host, host_port, channel_id))
                response_json = r.json()

                if response_json["del_response"]["response_code"] != 0:
                    return delete_channel_response("Channel successfully deleted but, was unable to delete messages", 0)

            return delete_channel_response("Channel successfully deleted", 0)

        except ValueError:
            return delete_channel_response("Invalid input", 1)
        except:
            return delete_channel_response("Unable to connect to the database", 1)

if __name__ == '__main__':
    conf = {
        "/channels": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
            "tools.response_headers.on": True,
            "tools.response_headers.headers": [("Content-Type", "application/json")]
            },
        "/": {
            }
        }

    app = Root()
    app.channels = ChannelWebService()

    cherrypy.config.update({'server.socket_port': slacker_config.urls.port['channels']})
    cherrypy.server.socket_host = slacker_config.urls.port['channels']
    cherrypy.quickstart(app, '/', conf)