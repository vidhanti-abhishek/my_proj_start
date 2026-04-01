# 🛠️ FixItGo: AI-Powered Service Booking Platform

FixItGo is a production-ready, modular service booking platform that connects users with nearby service providers (electricians, plumbers, mechanics, etc.) using AI-driven recommendations and a robust booking system.

## 🎯 Core Features

- **AI Service Recommendation Engine**: Analyzes user problem descriptions to predict service category, urgency, and estimated price.
- **Smart Worker Matching**: Ranks workers based on a weighted score of rating (50%), distance (30%), and availability (20%).
- **Real-Time Booking System**: Prevents double-booking with atomic slot management and status tracking.
- **Rating & Review System**: Allows users to rate and review completed services, influencing future recommendations.
- **Modular Architecture**: Clean separation of concerns with reusable services and components.

## 🏗️ System Architecture

### 1. Database Schema (SQLite)
- **users**: Customer profiles and contact info.
- **workers**: Service provider details, categories, and locations.
- **services**: Standardized service categories and price ranges.
- **availability_slots**: Time slots for workers with booking status.
- **bookings**: Transactional records linking users, workers, and slots.
- **reviews**: User feedback and ratings for completed bookings.

### 2. Project Structure
```text
fixitgo/
├── app.py                  # Main entry point (Gradio UI)
├── data/
│   ├── database.py         # DB connection and schema initialization
│   └── seed_db.py          # Sample data for testing
├── services/
│   ├── ai_recommender.py   # NLP-based problem analysis
│   ├── booking_service.py  # Slot and booking management
│   ├── recommendation_engine.py # Weighted worker scoring
│   └── review_service.py   # Rating and review logic
├── components/
│   ├── search_tab.py       # Search and AI analysis UI
│   ├── book_tab.py         # Booking flow UI
│   └── account_tab.py      # User history and reviews UI
└── utils/
    └── helpers.py          # Shared utility functions
```

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install gradio spacy transformers torch scikit-learn
python -m spacy download en_core_web_sm
```

### 2. Initialize and Seed Database
```bash
python fixitgo/data/database.py
python fixitgo/data/seed_db.py
```

### 3. Run the Application
```bash
python fixitgo/app.py
```

## 🔮 Future Improvements
- **Real-Time Notifications**: Email/SMS alerts for booking confirmations.
- **Payment Integration**: Stripe/PayPal for secure service payments.
- **Advanced NLP**: Fine-tune a BERT model on specific service datasets for higher accuracy.
- **Mobile App**: Convert the Gradio UI to a native mobile experience using React Native.
- **Geofencing**: Use real GPS coordinates and Google Maps API for precise distance calculation.

