import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS internships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        stipend TEXT,
        link TEXT UNIQUE,
        scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    print("Database initialized and 'internships' table created.")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()