from flask import Flask, render_template
import sqlite3
import requests

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("quotes.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS quotes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quote TEXT,
        author TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():

    try:
        response = requests.get(
            "https://dummyjson.com/quotes/random"
        )

        data = response.json()

        quote = data["quote"]
        author = data["author"]

    except:
        quote = "Success is the sum of small efforts repeated day in and day out."
        author = "Robert Collier"

    conn = sqlite3.connect("quotes.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO quotes(quote, author) VALUES (?, ?)",
        (quote, author)
    )

    conn.commit()

    cur.execute(
        "SELECT quote, author FROM quotes ORDER BY id DESC"
    )

    history = cur.fetchall()

    conn.close()

    return render_template(
        "index.html",
        quote=quote,
        author=author,
        history=history
    )

if __name__ == "__main__":
    app.run(debug=True)