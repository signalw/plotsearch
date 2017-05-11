from flask import *
from libs import se

app = Flask(__name__)
PER_PAGE = 10

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/results/p.<page>", methods=["POST"])
def results(page):
    page = int(page)
    res = se.search(request.form, (page-1)*PER_PAGE, page*PER_PAGE)
    return render_template(
        "results.html", page=page, form=request.form, results=res
    )

@app.route("/movie/<id>")
def movie(id):
    movie = se.search_by_id(id)
    return render_template("movie.html", movie=movie)

if __name__=="__main__":
    app.secret_key = 'random bytes :)'
    app.run(debug=True)
