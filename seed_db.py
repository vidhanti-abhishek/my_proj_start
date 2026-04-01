import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "fixitgo.db")

def seed_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Seed Users
    users = [
        ('John Doe', 'john@example.com', '1234567890'),
        ('Jane Smith', 'jane@example.com', '0987654321')
    ]
    cursor.executemany('INSERT OR IGNORE INTO users (name, email, phone) VALUES (?, ?, ?)', users)
    
    # 2. Seed Workers
    workers = [
        ('Alice Electric', 'Electrical', 75.0, 40.7128, -74.0060, 'Expert electrician with 10 years experience.'),
        ('Bob Plumber', 'Plumbing', 60.0, 40.7306, -73.9352, 'Fast and reliable plumbing services.'),
        ('Charlie AC', 'AC Repair', 90.0, 40.7580, -73.9855, 'Specialist in all AC brands and models.'),
        ('David Mechanic', 'Mechanic', 100.0, 40.7829, -73.9654, 'Mobile mechanic for your convenience.'),
        ('Eve Cleaner', 'Cleaning', 40.0, 40.7061, -74.0092, 'Professional home and office cleaning.')
    ]
    cursor.executemany('INSERT OR IGNORE INTO workers (name, category, base_price, location_lat, location_lon, bio) VALUES (?, ?, ?, ?, ?, ?)', workers)
    
    # 3. Seed Availability Slots (Next 3 days)
    cursor.execute('SELECT id FROM workers')
    worker_ids = [row[0] for row in cursor.fetchall()]
    
    slots = []
    now = datetime.now()
    for worker_id in worker_ids:
        for i in range(1, 4): # Next 3 days
            for hour in [9, 11, 14, 16]: # 4 slots per day
                slot_time = (now + timedelta(days=i)).replace(hour=hour, minute=0, second=0, microsecond=0)
                slots.append((worker_id, slot_time.strftime('%Y-%m-%d %H:%M:%S')))
                
    cursor.executemany('INSERT OR IGNORE INTO availability_slots (worker_id, slot_time) VALUES (?, ?)', slots)
    
    # 4. Seed some initial reviews
    reviews = [
        (1, 1, 1, 5, 'Excellent service, very professional!'),
        (2, 2, 2, 4, 'Good work, but arrived 10 minutes late.'),
        (3, 1, 3, 5, 'Fixed my AC in no time. Highly recommended!')
    ]
    # Note: These need valid booking IDs, but for seeding we can just insert directly into reviews
    # if we relax the foreign key constraint or create mock bookings first.
    # For simplicity, let's just seed the workers' initial ratings via a mock review table if needed,
    # but here we'll just ensure the workers exist.
    
    conn.commit()
    conn.close()
    print("Database seeded successfully.")

if __name__ == "__main__":
    seed_db()
