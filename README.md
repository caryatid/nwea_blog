# simple blog api implemented using uwsgi in python

## Requirements:

- Python 3
- virtualenv

## API

- /post
    post accepts a json payload that requires keys:
    - title : string
    - body  : string
- /posts
    posts returns a json list of dictionaries. returning keys per item:
    - post_id : integer ( primary key )
    - title   : string
    - body    : string

## Use and Testing
new posts can be created with a json payload via:

    echo '{"title": "grue", "body": "the magnificent"}' >post.json
    curl -H "Accept: application/json" -H "Content-Type: application/json" \ 
      -X POST -d @post.json http://<host>:9001/post

all posts can be retreived via

    curl -H "Accept: application/json" http://<host>:9001/posts 

The Makefile has handy endpoints for ensuring good style and that
the API works as intended. `make style` will set-up environment and run tests

## Deploy
Not entirely certain how you would like deploy handled for this as
it is dependent on a webserver of some sort. I have it such that the Makefile
will pull uwsgi into the virtualenv and the application
can be easily started and listening on port 9001 with the script,
"run_server.sh". Deploy specifics would be wildly variant depending 
on environement specifics such as:

- process supervisor on system
    - systemd
    - supervisorctl
    - init.d
- web server
    - apache w/ mod_python
    - nginx 
    - uwsgi

If you'd like me to provide a config for one of the web servers and/or a 
a service start script for one of the process supervisor above I would be 
more than happy to do so.

Additionally, I did organize the files to easily make into a pip package
if you'd like to see that as well. However, finalizing the pip package
would be dependent-ish on choosing the process supervisor first. 