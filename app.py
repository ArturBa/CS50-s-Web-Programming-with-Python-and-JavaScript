import os

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config.from_pyfile('app.config')

img = 0


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/mobile")
def mobile():
    return render_template('mobile.html')


@app.route("/desktop")
def desktop():
    return render_template('desktop.html')


@app.route("/save_img", methods=['POST'])
def save_img():
    global img
    img = request.form.get('img64')
    return jsonify({'status': 200})


@app.route('/get_img')
def get_img():
    response = {"img": img}
    return response


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
