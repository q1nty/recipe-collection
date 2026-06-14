from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "secret"
DB = "recipes.db"


def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            instructions TEXT NOT NULL,
            cooking_time TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def validate_form(form):
    return all([
        form.get("title"),
        form.get("category"),
        form.get("ingredients"),
        form.get("instructions"),
        form.get("cooking_time")
    ])


@app.route("/")
def index():
    search = request.args.get("search", "")

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    if search:
        c.execute("SELECT * FROM recipes WHERE title LIKE ?", ('%' + search + '%',))
    else:
        c.execute("SELECT * FROM recipes")

    recipes = c.fetchall()
    conn.close()

    return render_template("index.html", recipes=recipes)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":

        if not validate_form(request.form):
            flash("Заполните все поля!")
            return redirect("/add")

        conn = sqlite3.connect(DB)
        c = conn.cursor()

        c.execute("""
            INSERT INTO recipes (title, category, ingredients, instructions, cooking_time)
            VALUES (?, ?, ?, ?, ?)
        """, (
            request.form["title"],
            request.form["category"],
            request.form["ingredients"],
            request.form["instructions"],
            request.form["cooking_time"]
        ))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add_recipe.html")


@app.route("/recipe/<int:id>")
def recipe(id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM recipes WHERE id=?", (id,))
    recipe = c.fetchone()
    conn.close()

    return render_template("recipe.html", recipe=recipe)


@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("DELETE FROM recipes WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    if request.method == "POST":
        c.execute("""
            UPDATE recipes
            SET title=?, category=?, ingredients=?, instructions=?, cooking_time=?
            WHERE id=?
        """, (
            request.form["title"],
            request.form["category"],
            request.form["ingredients"],
            request.form["instructions"],
            request.form["cooking_time"],
            id
        ))

        conn.commit()
        conn.close()
        return redirect("/")

    c.execute("SELECT * FROM recipes WHERE id=?", (id,))
    recipe = c.fetchone()
    conn.close()

    return render_template("edit_recipe.html", recipe=recipe)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)