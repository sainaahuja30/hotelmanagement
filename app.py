from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            room_type TEXT,
            check_in TEXT,
            check_out TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        name = request.form['name']
        room_type = request.form['room_type']
        check_in = request.form['check_in']
        check_out = request.form['check_out']
        
        conn = sqlite3.connect('hotel.db')
        c = conn.cursor()
        c.execute('INSERT INTO bookings (name, room_type, check_in, check_out) VALUES (?, ?, ?, ?)',
                  (name, room_type, check_in, check_out))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('booking.html')

@app.route('/admin')
def admin():
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    c.execute('SELECT * FROM bookings')
    bookings = c.fetchall()
    conn.close()
    return render_template('view_bookings.html', bookings=bookings)

if __name__== "__main__":
    init_db()
    app.run(debug=True)
