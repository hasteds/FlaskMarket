from flask import Flask, render_template, redirect, request

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Hello Tin and Daria</h1>"


@app.route("/about/<username>")
def about(username):
    return f"<h1>This is about page of {username} </h1>"