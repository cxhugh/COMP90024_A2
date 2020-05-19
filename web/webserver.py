from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def COMP90024_home():
    return render_template("index.html")

# @app.route('/contact')
# def contact():
#     return render_template("contact.html")

# @app.route('/melbourne')
# def greater_melbourne():
#     return render_template("melbourne.html")

# @app.route('/big-cites')
# def whole_australia():
#     return render_template("big-cites.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000)