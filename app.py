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

@app.route("/movie/<id>")
def movie(id):
    movie = se.search_by_id(id)
    return render_template("movie.html", movie=movie)

if __name__=="__main__":
    app.run(debug=True)
