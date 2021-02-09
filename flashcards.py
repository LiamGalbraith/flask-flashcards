from flask import (
    Flask,
    render_template,
    abort,
    jsonify,
    request,
    redirect,
    url_for,
    send_file
)

from model import save_db, load_db

db = load_db()
app = Flask(
    __name__
)  # Creates a global Flask application object with the name of the current module (flashcards)


@app.route("/", methods=["GET", "POST"])
def welcome():
    if request.method == "POST":
        f = request.files["file"]
        f.save("flashcards_db.json")
        global db
        db = load_db()

    return render_template("welcome.html", cards=db)


# export FLASK_APP=flashcards.py  # location of module containing app
# export FLASK_ENV=development  # Tell flask you're running in dev and starts the debugger. Never use in production.
# flask run


@app.route("/card/<int:index>")
def card_view(index):
    try:
        card = db[index]
        return render_template(
            "card.html", card=card, index=index, max_index=len(db) - 1
        )
    except IndexError:
        abort(404)


@app.route("/add_card", methods=["GET", "POST"])
def add_card():
    if request.method == "POST":
        card = {
            "question": request.form['question'],
            "answer": request.form['answer']
        }
        db.append(card)
        save_db()

        return redirect(url_for('card_view', index=len(db) - 1))

    elif request.method == "GET":
        return render_template("add_card.html")


@app.route("/remove_card/<int:index>", methods=["GET", "POST"])
def remove_card(index):
    try:
        if request.method == "GET":
            return render_template("remove_card.html", card=db[index])

        elif request.method == "POST":
            del db[index]
            save_db()

            return redirect((url_for("welcome")))
    except IndexError:
        abort(404)


@app.route("/api/card/")
def api_card_list():
    return jsonify(db)


@app.route("/api/card/<int:index>")
def api_card_detail(index):
    try:
        return db[index]
    except IndexError:
        abort(404)


@app.route("/download")
def download_file():
    save_db()
    return send_file('flashcards_db.json', as_attachment=True)
