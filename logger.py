from pprint import pprint

'''
logger.py

# Wrapper class for app.py to log HTTP requests/responses

@ethanpinter
'''

class Logger(object):
    def __init__(self, app):
        self._app = app
        
    def __call__(self, env, resp):
        errorlog = env['wsgi.errors']
        with open('request.data', 'wt') as errorlog:
            pprint(('REQUEST', env), stream=errorlog)
           
        def log_response(status, headers, *args):
            with open('response.data', 'wt') as errorlog:
                pprint(('RESPONSE', status, headers), stream=errorlog)
            return resp(status, headers, *args)
        
        return self._app(env, log_response)
