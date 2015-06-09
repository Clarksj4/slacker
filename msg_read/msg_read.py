__author__ = 'ping.dong'

import cherrypy
import httplib2 as http
import json
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

# Service endpoint define
# TODO: Service Endpoint should retrieve dynamically
auth_service_url = ''
auth_key_param = '{"credential","{0}"}'
auth_permission_param = '{"credential","{0}"}'

msg_service_url = ''
msg_read_param = '{"channel_id","{0}";"offset","{1}"}'

class MessageReadService:
    exposed = True

    def __init__(self):
        pass

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        try:
            # check argument
            parameters = cherrypy.request.json
            credential = paramters['key']
            channel_id = int(parameters['channel_id'])
            offset = int(parameters['offset'])
        except ValueError:
            return {'error': 'invalid data format'}

        try:
            # authenticate
            auth_param = auth_key_param.format(credential)
            auth_response_content = self.call_rest_api(auth_service_url, auth_param)
            auth_result = json.load(auth_response_content)
            # Check auth result
            try:
                if not self.str2bool(auth_result['valid']):
                    return {'error', 'unauthorized'}
            except:  # should capture more specific exception
                return {'error', 'unauthorized'}

            # authorize
            #permission_param = auth_key_param.format(credential)
            #permission_response_content = self.call_rest_api(auth_service_url, permission_param)
            #permission = json.load(permission_response_content)
            # check permission here

            # pass-through data
            msg_param = msg_read_param.format(channel_id, offset)
            msg_response_content = self.call_rest_api(msg_service_url, msg_param)
            msg = json.load(msg_response_content)
            return msg
        except: # should capture more specific exception
            return {'error': 'Unexpected error'}

    def str2bool(self, v):
        return v.lower() in ("yes", "true", "t", "1")

    def call_rest_api(self, url, message):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8'
        }

        target = urlparse(url)
        method = 'GET'

        h = http.Http()

        #if auth:
        #    h.add_credentials(credential)

        response, content = h.request(
            target.geturl(),
            method,
            message,
            headers)

        return content

if __name__ == '__main__':
    conf = {
        "/": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
            "tools.response_headers.on": True,
            "tools.response_headers.headers": [("Content-Type", "application/json")]
            }
        }
    cherrypy.config.update({'server.socket_port': 8000})
    cherrypy.quickstart(MessageReadService(), '/', conf)
