from database import get_db_connection
import logging

logger = logging.getLogger(__name__)

class BookingService:
    @staticmethod
    def get_available_slots(worker_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, slot_time FROM availability_slots 
            WHERE worker_id = ? AND is_booked = 0
            ORDER BY slot_time ASC
        ''', (worker_id,))
        slots = cursor.fetchall()
        conn.close()
        return slots

    @staticmethod
    def create_booking(user_id, worker_id, slot_id, problem_description):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # 1. Check if slot is still available (Atomic check)
            cursor.execute('SELECT is_booked FROM availability_slots WHERE id = ?', (slot_id,))
            slot = cursor.fetchone()
            if not slot or slot['is_booked'] == 1:
                return False, "Slot is no longer available."

            # 2. Create booking
            cursor.execute('''
                INSERT INTO bookings (user_id, worker_id, slot_id, problem_description, status)
                VALUES (?, ?, ?, ?, 'Pending')
            ''', (user_id, worker_id, slot_id, problem_description))
            
            # 3. Mark slot as booked
            cursor.execute('UPDATE availability_slots SET is_booked = 1 WHERE id = ?', (slot_id,))
            
            conn.commit()
            return True, "Booking created successfully!"
        except Exception as e:
            conn.rollback()
            logger.error(f"Booking error: {e}")
            return False, f"An error occurred: {str(e)}"
        finally:
            conn.close()

    @staticmethod
    def get_user_bookings(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT b.id, w.name as worker_name, w.category, b.status, a.slot_time, b.problem_description
            FROM bookings b
            JOIN workers w ON b.worker_id = w.id
            JOIN availability_slots a ON b.slot_id = a.id
            WHERE b.user_id = ?
            ORDER BY a.slot_time DESC
        ''', (user_id,))
        bookings = cursor.fetchall()
        conn.close()
        return bookings

    @staticmethod
    def update_booking_status(booking_id, status):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE bookings SET status = ? WHERE id = ?', (status, booking_id))
        conn.commit()
        conn.close()
        return True
