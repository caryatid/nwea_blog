make bootstrap
source .virt/bin/activate
uwsgi --http :9001 --wsgi-file nwea_blog/blog.py
