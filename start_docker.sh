#!/bin/bash

nohup python /server.py &

/usr/lib/postgresql/9.3/bin/postgres -D /etc/postgresql/9.3/main

