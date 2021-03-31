from flask import render_template
from pikaia import app


@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")
