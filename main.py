#!/usr/bin/env python3
from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)
