from flask import Flask, render_template
from dbmModules.CtaWebFunctions import *

ctaWebInterface = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/output",methods=["POST"])
def scriptOutput():
    if request.method == "POST":
        script = request.form[someformnameneedsaddingherewhenformismade]
        response = webScriptRefinementChecker(str(script))
        return render_template(#someoutputpagegoeshere,#someelement=response)
    else:
        return #someerrorcondition


if __name__ == "__main__":
    ctaWebInterface.run(threaded=True)