from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("recipes.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
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

@app.route("/")
def index():
    search = request.args.get("search", "")
    conn = get_db()

    if search:
        recipes = conn.execute(
            "SELECT * FROM recipes WHERE title LIKE ?",
            (f"%{search}%",)
        ).fetchall()
    else:
        recipes = conn.execute(
            "SELECT * FROM recipes"
        ).fetchall()

    conn.close()
    return render_template("index.html", recipes=recipes)

@app.route("/add", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        conn = get_db()
        conn.execute("""
            INSERT INTO recipes
            (title, category, ingredients, instructions, cooking_time)
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
    conn = get_db()
    recipe = conn.execute(
        "SELECT * FROM recipes WHERE id=?",
        (id,)
    ).fetchone()
    conn.close()

    if recipe is None:
        return "Recipe not found", 404

    return render_template("recipe.html", recipe=recipe)

@app.route("/delete/<int:id>")
def delete_recipe(id):
    conn = get_db()
    conn.execute(
        "DELETE FROM recipes WHERE id=?",
        (id,)
    )
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)