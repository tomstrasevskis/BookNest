from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Konfigurācija
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Savienojums ar datubāzi
def get_db_connection():
    conn = sqlite3.connect('db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

# Sākumlapa – grāmatu saraksts
@app.route('/')
def index():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return render_template('index.html', books=books)

# Grāmatas detalizēta lapa + komentēšana
@app.route('/book/<int:id>', methods=['GET', 'POST'])
def book_detail(id):
    conn = get_db_connection()
    if request.method == 'POST':
        content = request.form['content']
        conn.execute('INSERT INTO comments (user_id, book_id, content) VALUES (?, ?, ?)', (1, id, content))  # user_id = 1 kā tests
        conn.commit()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (id,)).fetchone()
    comments = conn.execute('SELECT * FROM comments WHERE book_id = ?', (id,)).fetchall()
    conn.close()
    return render_template('book_detail.html', book=book, comments=comments)

# Pievienot jaunu grāmatu
@app.route('/add', methods=('GET', 'POST'))
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        description = request.form['description']

        image = request.files['image']
        image_filename = ''
        if image and image.filename:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_filename = filename

        conn = get_db_connection()
        conn.execute('INSERT INTO books (title, author, description, image) VALUES (?, ?, ?, ?)',
                     (title, author, description, image_filename))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_book.html')

# Rediģēt esošu grāmatu
@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_book(id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (id,)).fetchone()
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        description = request.form['description']
        conn.execute('UPDATE books SET title = ?, author = ?, description = ? WHERE id = ?',
                     (title, author, description, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('edit_book.html', book=book)

# Dzēst grāmatu
@app.route('/delete/<int:id>')
def delete_book(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM books WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Dzēst komentāru
@app.route('/delete_comment/<int:comment_id>/<int:book_id>')
def delete_comment(comment_id, book_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM comments WHERE id = ?', (comment_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('book_detail', id=book_id))

# Palaist lietotni
if __name__ == '__main__':
    app.run(debug=True)
