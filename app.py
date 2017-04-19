from flask import *
from libs import se

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/results", methods=["POST"])
def results():
    res = se.search()
    return render_template("results.html", results=res)

if __name__=="__main__":
    app.run(debug=True)
