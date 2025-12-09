from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ---------- Initialize DB ----------
def init_db():
    conn = sqlite3.connect('feedback.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.close()

init_db()

# ---------- Home Page ----------
@app.route('/')
def index():
    return render_template('index.html')

# ---------- Submit Feedback ----------
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    conn = sqlite3.connect('feedback.db')
    conn.execute("INSERT INTO feedback (name, email, message) VALUES (?, ?, ?)", (name, email, message))
    conn.commit()
    conn.close()

    return redirect('/')

# ---------- View Feedback ----------
@app.route('/view')
def view():
    conn = sqlite3.connect('feedback.db')
    cursor = conn.execute("SELECT * FROM feedback")
    data = cursor.fetchall()
    conn.close()

    return render_template('view.html', feedback=data)

if __name__ == '__main__':
    app.run(debug=True)
