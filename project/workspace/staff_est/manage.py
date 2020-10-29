#!/usr/bin/env python
import os
import sys

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geodjango_test.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
    
