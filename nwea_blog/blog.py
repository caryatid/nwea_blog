import codecs
import json
import sqlite3


INSERT_POST_SQL='''
INSERT INTO posts (post_id, title, body) VALUES (?,?,?)
'''.strip()


LIST_POSTS_SQL='''
SELECT post_id, title, body FROM posts;
'''.strip()


# I think the schema should be changed to have post_id disallow NULL.
# inserts do not increment w/o explicit post_id set.
# I suspect making the primary key an explicit INTEGER fixes
MAX_ID_SQL='''
SELECT MAX(post_id) from posts;
'''.strip()


def post(environ, c):
    reader = codecs.getreader('utf-8')
    p_data = json.load(reader(environ['wsgi.input']))
    i = c.execute(MAX_ID_SQL).fetchone()[0] or 0
    c.execute(INSERT_POST_SQL, (i + 1, p_data['title'], p_data['body']))
    return json.dumps({'body': 'Inserted blog post: {}'.format(p_data['title'])})


def posts(c):
    r_names = ['post_id', 'title', 'body']  # names from sql columns?
    retval = []
    for r in c.execute(LIST_POSTS_SQL):
        retval.append({k: v for k, v in zip(r_names, r)})
    return json.dumps(retval)


def route(environ, endpoint):
    status = '200 OK'
    cmd = endpoint[0]
    with sqlite3.connect('blog.db') as conn:
        if cmd == 'post':
            response = post(environ, conn.cursor())
        elif cmd == 'posts':
            response = posts(conn.cursor())
        else:
            status = '404 Not found'
            response = json.dumps({'body': 'Nothing here, friends'})
    return (status, response)


def application(environ, start_response):
    response_headers = [('Content-Type', 'application/json')]
    l = [x.lower() for x in environ['PATH_INFO'][1:].split('/')]
    l = ['posts'] if not l else l  # list incase of future endpoints
    try:
        status, response = route(environ, l)
    except Exception as e:
        status = '500 Unknown server error'
        response = json.dumps({'body': e})
    start_response(status, response_headers)
    return codecs.encode(response)