import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)
DATABASE = "scores.db"
