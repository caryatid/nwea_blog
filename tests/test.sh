#!/bin/sh

# prolly ought to randomize port for simultaneous runs
uwsgi --http :9001 --wsgi-file nwea_blog/blog.py >/dev/null 2>&1 &
WSGI_PID=$!
TMP=$(mktemp -d)

trap "rm -Rf $TMP" EXIT

cat <<EOF >$TMP/json.1
{"body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit",
"title": "lorem"}
EOF

cat <<EOF >$TMP/json.2
{"title": "foo", "body": "bar"}
EOF

cat <<EOF >$TMP/json.3
{"title": "nwea",
 "body": "This is an example program
 showing a simple api for POST/GET of blog posts. It may be interesting
 to add a PUT endpoint. Meaning an idempotent push of data, perhaps matching
 on 'title'"}
EOF

echo posting
echo -------
for f in $(ls $TMP/json*)
do
    curl -H 'Content-Type: application/json' -X POST -d "@$f" http://localhost:9001/post
    echo
done
echo getting posts
echo -------------
curl -H 'Accept: application:json' http://localhost:9001/posts
 
kill $WSGI_PID
echo

wait