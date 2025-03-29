# app.py

from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize Database
def init_db():
    conn = sqlite3.connect('dietplan.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS health_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        condition TEXT,
                        weight INTEGER,
                        allergies TEXT,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )''')
    conn.commit()
    conn.close()

init_db()

# Route: Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Route: User Registration
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    try:
        conn = sqlite3.connect('dietplan.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    except sqlite3.IntegrityError:
        return "Username already exists. Try again."

# Route: User Login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect('dietplan.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['user_id'] = user[0]
        return redirect(url_for('health'))
    else:
        return "Invalid login. Try again."

# Route: Health Data Submission
@app.route('/submit_health', methods=['POST'])
def submit_health():
    if 'user_id' not in session:
        return redirect(url_for('home'))

    condition = request.form['condition']
    weight = request.form['weight']
    allergies = request.form['allergies']

    conn = sqlite3.connect('dietplan.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO health_data (user_id, condition, weight, allergies) VALUES (?, ?, ?, ?)", (session['user_id'], condition, weight, allergies))
    conn.commit()
    conn.close()

    return redirect(url_for('diet_plan'))

# Route: Diet Plan Generation
@app.route('/diet_plan')
def diet_plan():
    if 'user_id' not in session:
        return redirect(url_for('home'))

    conn = sqlite3.connect('dietplan.db')
    cursor = conn.cursor()
    cursor.execute("SELECT condition, weight, allergies FROM health_data WHERE user_id=?", (session['user_id'],))
    health_data = cursor.fetchone()
    conn.close()

    if health_data:
        condition, weight, allergies = health_data
        plan = f"Custom Diet Plan for {condition}: \n- Breakfast: Oatmeal\n- Lunch: Grilled Chicken\n- Dinner: Salad"
    else:
        plan = "No health data available."

    return f"<h2>Your Diet Plan</h2><pre>{plan}</pre>"

# Route: Chatbot (Basic Response)
@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.form['message']
    return f"Bot: I am here to help with your diet plan. You said: {user_input}"

# Route: Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

                    