from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def home():
    return render_template("index.html")

@app.route('/contact.html')
def contact():
    return render_template("contact.html")

@app.route('/melbourne.html')
def melbourne():
    return render_template("melbourne.html")

@app.route('/big-cites.html')
def big_cites():
    return render_template("big-cities.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000)