from flask import Flask, render_template, request, url_for, redirect
from dbmModules.CtaWebFunctions import *

ctaWebInterface = Flask(__name__)

@app.route("/",methods=["POST","GET"])
def home():
    if request.method == "POST":
        scriptInput = request.form["script"]
        response = webScriptRefinementChecker(str(scriptInput))
        return redirect(url_for("ouput",script = response))
    else:
        return render_template("index.html")

@app.route("/output")
def output(script):
    return "<h1>{script}</h1>"


if __name__ == "__main__":
    ctaWebInterface.run(threaded=True)
