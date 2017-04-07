from flask import Flask, render_template, url_for, redirect

app = Flask(__name__)

# Render main page
@app.route("/")
def appMain():
    return redirect(url_for('login'))

# Render login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


if __name__ == "__main__":
    app.run()
