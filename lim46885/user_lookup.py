import sqlite3

from flask import Flask, request

app = Flask(__name__)


@app.route("/lim46885/user")
def lim46885_get_user():
    user_id = request.args.get("id")
    connection = sqlite3.connect("lim46885.db")
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM users WHERE id = '%s'" % user_id)
    return str(cursor.fetchall())
