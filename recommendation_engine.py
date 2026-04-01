from database import get_db_connection
from review_service import ReviewService
import math
import logging

logger = logging.getLogger(__name__)

class RecommendationEngine:
    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        # Simple Euclidean distance for mock purposes
        return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

    @staticmethod
    def get_recommended_workers(category, user_lat=0.0, user_lon=0.0):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 1. Get all workers in the category
        cursor.execute('''
            SELECT id, name, category, base_price, location_lat, location_lon, bio
            FROM workers
            WHERE category = ?
        ''', (category,))
        workers = cursor.fetchall()
        
        # 2. Get availability for each worker
        cursor.execute('''
            SELECT worker_id, COUNT(id) as available_slots
            FROM availability_slots
            WHERE is_booked = 0
            GROUP BY worker_id
        ''')
        availability_map = {row['worker_id']: row['available_slots'] for row in cursor.fetchall()}
        
        # 3. Calculate scores for each worker
        scored_workers = []
        for worker in workers:
            worker_id = worker['id']
            
            # Get rating and review count
            avg_rating, total_reviews = ReviewService.get_worker_rating(worker_id)
            
            # Distance score (normalized 0-1, where 1 is closest)
            distance = RecommendationEngine.calculate_distance(
                user_lat, user_lon, worker['location_lat'], worker['location_lon']
            )
            distance_score = 1 / (1 + distance) # Simple normalization
            
            # Availability score (normalized 0-1)
            slots = availability_map.get(worker_id, 0)
            availability_score = 1 if slots > 0 else 0
            
            # Weighted scoring: (rating * 0.5) + (distance_score * 0.3) + (availability * 0.2)
            # Normalize rating to 0-1 scale (rating / 5)
            normalized_rating = avg_rating / 5.0
            
            score = (normalized_rating * 0.5) + (distance_score * 0.3) + (availability_score * 0.2)
            
            scored_workers.append({
                "id": worker_id,
                "name": worker['name'],
                "category": worker['category'],
                "base_price": worker['base_price'],
                "avg_rating": avg_rating,
                "total_reviews": total_reviews,
                "distance": round(distance, 2),
                "available_slots": slots,
                "score": round(score, 4),
                "bio": worker['bio']
            })
            
        # 4. Sort by score descending
        scored_workers.sort(key=lambda x: x['score'], reverse=True)
        
        conn.close()
        return scored_workers
