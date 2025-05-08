import sqlite3

with open('schema.sql', 'r', encoding='utf-8') as f:
    sql_script = f.read()

conn = sqlite3.connect('db.sqlite')
conn.executescript(sql_script)

# Lietotājs
conn.execute("INSERT INTO users (name, email) VALUES (?, ?)", ('Test Lietotājs', 'test@example.com'))

# Grāmatas
conn.execute("INSERT INTO books (title, author, description, image) VALUES (?, ?, ?, ?)",
             ('Zudušie Vārdi', 'A. Rakstnieks', 'Grāmata par piedzīvojumu pasaulē bez vārdiem.', ''))
conn.execute("INSERT INTO books (title, author, description, image) VALUES (?, ?, ?, ?)",
             ('Sapņu Mežs', 'B. Sapņotājs', 'Noslēpumains mežs, kur viss ir iespējams.', ''))

# Komentāri
conn.execute("INSERT INTO comments (user_id, book_id, content) VALUES (?, ?, ?)", (1, 1, 'Ļoti interesants sižets!'))
conn.execute("INSERT INTO comments (user_id, book_id, content) VALUES (?, ?, ?)", (1, 2, 'Man ļoti patika šī pasaule.'))

conn.commit()
conn.close()

print("✅ Database created with placeholder books and comments!")
