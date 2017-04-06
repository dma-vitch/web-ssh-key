from flask import Flask, render_template, url_for, redirect, jsonify, request, g, session, flash
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

# Render login page
@app.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template('login.html')


if __name__ == "__main__":
    app.run()