import json
import sqlite3

# does sqlite allow `with` context for cursors?
conn = sqlite3.connection('blog.db')

def post_stream():
    pass

def get_stream():
    pass

# non stream GET/POST?

def route(environ, endpoint):
    cmd = endpoint[0]
    if cmd == 'post':
        pass
    elif cmd == 'posts':
    else:
        status = '404 Not found'
        response = ['Nothing here, friends']
    pass


def application(environ, start_response):
    response_headers = [('Content-type', 'application/json')]
    l = [x.lower() for x in environ['PATH_INFO'][1:].split('/')]
    l = ['posts'] if not l else l  # list incase of future endpoints
    pass
