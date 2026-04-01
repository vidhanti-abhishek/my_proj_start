# 🛠️ FixItGo – AI-Powered Service Booking Platform

FixItGo is an AI-powered platform that connects users with nearby service professionals like electricians, plumbers, and mechanics using smart recommendations and real-time booking.

---

## 🚀 Features

- 🤖 AI-based service recommendation (NLP)
- 📍 Smart worker matching (rating, distance, availability)
- ⚡ Real-time booking system (no double booking)
- ⭐ Rating & review system
- 🧩 Modular and scalable architecture

---

## 🏗️ System Overview

### Database (SQLite)
- users – customer data  
- workers – service providers  
- services – categories and pricing  
- availability_slots – worker schedules  
- bookings – service transactions  
- reviews – ratings and feedback  

---

## 📂 Project Structure
fixitgo/
├── app.py
├── data/
│ ├── database.py
│ └── seed_db.py
├── services/
│ ├── ai_recommender.py
│ ├── booking_service.py
│ ├── recommendation_engine.py
│ └── review_service.py
├── components/
│ ├── search_tab.py
│ ├── book_tab.py
│ └── account_tab.py
└── utils/
└── helpers.py



---

## 🛠️ Tech Stack

- Python  
- Gradio  
- SQLite  
- spaCy  
- Transformers  
- Scikit-learn  

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash id="dep-install"
pip install gradio spacy transformers torch scikit-learn
python -m spacy download en_core_web_sm


2. Setup Database
python fixitgo/data/database.py
python fixitgo/data/seed_db.py
3. Run Application
python fixitgo/app.py
🔮 Future Scope
💳 Payment integration (Stripe/Razorpay)
📲 Real-time notifications
📍 Live GPS tracking (Google Maps API)
📱 Mobile app (React Native)
🧠 Advanced AI models
🎯 Vision

To build a smart and reliable platform for booking everyday services quickly using AI and real-time systems.

🤝 Contributing

Contributions are welcome! Feel free to fork and submit a pull request.

📄 License

MIT License

👨‍💻 Author

Abhishek kuamr 
Aspiring Software Develope | AI Enthusiast|   data scientist 🚀


---

## 🔥 This README is good because:
- Clean & professional ✅  
- ATS / recruiter friendly ✅  
- Startup-ready ✅  
- Easy to understand ✅  

---

If you want next 🚀  
I can:
- add **badges (stars, license, build status)** ⭐  
- create **demo screenshots section** 📸  
- or make your repo look like **top GitHub projects**

Just tell me 👍
