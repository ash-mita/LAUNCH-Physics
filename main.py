#!/usr/bin/env python3

from launch_physics import app
from os import environ

host = '0.0.0.0'
port = int(environ.get('PORT', 5000))
app.run(debug=True, host=host, port=port)
