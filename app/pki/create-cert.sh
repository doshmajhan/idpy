#!/bin/bash
set -x

openssl req -nodes -newkey rsa:2048 -keyout key.pem -out server.csr -subj "/C=US/ST=NY/L=NYC/O=idpy/OU=idpy/CN=idpy.com"
chmod 600 key.pem
openssl x509 -req -days 365 -in server.csr -signkey key.pem -out cert.pem