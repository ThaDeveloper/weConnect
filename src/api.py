import json
from flask import Flask
from flask import Flask, Response, abort
import os 
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


# from user import User
# from business import Business
# from review import Review

app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True)