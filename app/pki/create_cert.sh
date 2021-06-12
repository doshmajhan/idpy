#!/bin/bash

openssl genrsa -out key.pem 2048
chmod 600 server.key
openssl req -new -key key.pem -out server.csr
openssl x509 -req -days 365 -in server.csr -signkey key.pem -out cert.pem