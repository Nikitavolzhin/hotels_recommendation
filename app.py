from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap4
from forms import HotelRequestForm
from model import recommender


app = Flask(__name__)
bootstrap = Bootstrap4(app)
app.secret_key = "put_your_secret_key_here"


@app.route('/', methods=["GET", "POST"])
def index():
    form = HotelRequestForm()
    if form.validate_on_submit():
        wants: str = form.want_to_have.data
        avoids: str = form.want_to_avoid.data
        rating: str = form.rating.data

        return redirect(url_for("show", wants=wants, avoids=avoids, rating=rating))
    return render_template("index.html", form=form)


@app.route("/show", methods=["GET"])
def show():
    wants: str = request.args.get("wants")
    avoids: str = request.args.get("avoids")
    rating: str = request.args.get("rating")
    recommended = list(zip(*recommender(wants, avoids)))
    hotels = [hotel for hotel in recommended if hotel[1] > float(rating)] if rating else recommended

    return render_template("hotels.html", recommended=hotels, rating=rating)


if __name__ == '__main__':
    app.run()
