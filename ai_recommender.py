import spacy 
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIRecommender:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except Exception as e:
            logger.error(f"Failed to load spaCy model: {e}")
            self.nlp = None
            
        # Keyword-based fallback rules
        self.category_keywords = {
            "AC Repair": ["ac", "air conditioner", "cooling", "ventilation", "hvac", "filter"],
            "Plumbing": ["leak", "pipe", "tap", "faucet", "drain", "toilet", "water", "sink"],
            "Electrical": ["wire", "plug", "switch", "light", "fuse", "circuit", "power", "electricity"],
            "Mechanic": ["car", "engine", "brake", "tire", "oil", "battery", "transmission", "vehicle"],
            "Cleaning": ["dust", "mop", "sweep", "vacuum", "wash", "stain", "carpet", "window"]
        }
        
        self.urgency_keywords = {
            "High": ["emergency", "urgent", "asap", "now", "broken", "burst", "fire", "smoke", "flood"],
            "Medium": ["soon", "today", "tomorrow", "fix", "issue", "problem"],
            "Low": ["maintenance", "checkup", "quote", "later", "next week"]
        }

    def predict_category(self, text):
        text = text.lower()
        
        # 1. Rule-based keyword matching (Fast and reliable for specific terms)
        for category, keywords in self.category_keywords.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        # 2. NLP-based matching (Semantic similarity if model is loaded)
        if self.nlp:
            doc = self.nlp(text)
            best_category = "General Maintenance"
            max_similarity = 0
            
            for category in self.category_keywords.keys():
                cat_doc = self.nlp(category)
                similarity = doc.similarity(cat_doc)
                if similarity > max_similarity:
                    max_similarity = similarity
                    best_category = category
            
            if max_similarity > 0.5:
                return best_category
                
        return "General Maintenance"

    def predict_urgency(self, text):
        text = text.lower()
        for urgency, keywords in self.urgency_keywords.items():
            if any(keyword in text for keyword in keywords):
                return urgency
        return "Medium"

    def estimate_price_range(self, category):
        # Mock price ranges based on category
        price_map = {
            "AC Repair": (50, 200),
            "Plumbing": (40, 150),
            "Electrical": (60, 250),
            "Mechanic": (80, 500),
            "Cleaning": (30, 100),
            "General Maintenance": (40, 120)
        }
        return price_map.get(category, (50, 150))

    def analyze_problem(self, problem_text):
        if not problem_text or len(problem_text.strip()) < 3:
            return {
                "category": "Unknown",
                "urgency": "Low",
                "price_range": (0, 0),
                "message": "Please provide more details about your problem."
            }
            
        category = self.predict_category(problem_text)
        urgency = self.predict_urgency(problem_text)
        price_range = self.estimate_price_range(category)
        
        return {
            "category": category,
            "urgency": urgency,
            "price_range": price_range,
            "message": f"Based on your description, this looks like a {category} issue with {urgency} urgency."
        }

# Singleton instance
recommender = AIRecommender()
