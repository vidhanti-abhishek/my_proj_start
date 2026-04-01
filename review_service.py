from database import get_db_connection
import logging

logger = logging.getLogger(__name__)

class ReviewService:
    @staticmethod
    def add_review(booking_id, user_id, worker_id, rating, comment):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # 1. Check if booking exists and is completed
            cursor.execute('SELECT status FROM bookings WHERE id = ?', (booking_id,))
            booking = cursor.fetchone()
            if not booking or booking['status'] != 'Completed':
                return False, "Only completed bookings can be reviewed."

            # 2. Check if review already exists
            cursor.execute('SELECT id FROM reviews WHERE booking_id = ?', (booking_id,))
            if cursor.fetchone():
                return False, "Review already exists for this booking."

            # 3. Insert review
            cursor.execute('''
                INSERT INTO reviews (booking_id, user_id, worker_id, rating, comment)
                VALUES (?, ?, ?, ?, ?)
            ''', (booking_id, user_id, worker_id, rating, comment))
            
            conn.commit()
            return True, "Review added successfully!"
        except Exception as e:
            conn.rollback()
            logger.error(f"Review error: {e}")
            return False, f"An error occurred: {str(e)}"
        finally:
            conn.close()

    @staticmethod
    def get_worker_rating(worker_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT AVG(rating) as avg_rating, COUNT(id) as total_reviews
            FROM reviews
            WHERE worker_id = ?
        ''', (worker_id,))
        result = cursor.fetchone()
        conn.close()
        
        avg_rating = round(result['avg_rating'], 1) if result['avg_rating'] else 0.0
        total_reviews = result['total_reviews'] if result['total_reviews'] else 0
        
        return avg_rating, total_reviews

    @staticmethod
    def get_worker_reviews(worker_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT r.rating, r.comment, u.name as user_name, r.created_at
            FROM reviews r
            JOIN users u ON r.user_id = u.id
            WHERE r.worker_id = ?
            ORDER BY r.created_at DESC
        ''', (worker_id,))
        reviews = cursor.fetchall()
        conn.close()
        return reviews
