import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "fixitgo.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Workers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS workers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        base_price REAL,
        location_lat REAL,
        location_lon REAL,
        bio TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Services table (Categories and standard rates)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        min_price REAL,
        max_price REAL
    )
    ''')
    
    # Availability slots
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS availability_slots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        worker_id INTEGER,
        slot_time TIMESTAMP NOT NULL,
        is_booked INTEGER DEFAULT 0,
        FOREIGN KEY (worker_id) REFERENCES workers (id),
        UNIQUE(worker_id, slot_time)
    )
    ''')
    
    # Bookings table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        worker_id INTEGER,
        slot_id INTEGER,
        status TEXT CHECK(status IN ('Pending', 'Accepted', 'Rejected', 'Completed')) DEFAULT 'Pending',
        problem_description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (worker_id) REFERENCES workers (id),
        FOREIGN KEY (slot_id) REFERENCES availability_slots (id)
    )
    ''')
    
    # Reviews table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        booking_id INTEGER UNIQUE,
        user_id INTEGER,
        worker_id INTEGER,
        rating INTEGER CHECK(rating >= 1 AND rating <= 5),
        comment TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (booking_id) REFERENCES bookings (id),
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (worker_id) REFERENCES workers (id)
    )
    ''')
    
    # Indexes for performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_workers_category ON workers(category)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_availability_worker ON availability_slots(worker_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_bookings_user ON bookings(user_id)')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
