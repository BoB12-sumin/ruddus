from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    arrlist = ["a", "b", "c", "d", "e"]
    return render_template("ctfindex.html", content=arrlist)


@app.route("/about", methods=["GET", "POST"])
def about():
    if request.method == "POST":
        user = request.form["name"]
        print(user)

    return render_template("about.html", content=["user1", "user2", "user3"])


if __name__ == "__main__":
    app.run(debug=True)
