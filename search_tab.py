import gradio as gr
from ai_recommender import recommender
from recommendation_engine import RecommendationEngine

def search_workers(problem_text):
    if not problem_text or len(problem_text.strip()) < 3:
        return "Please describe your problem.", []
    
    # 1. AI Analysis
    analysis = recommender.analyze_problem(problem_text)
    category = analysis['category']
    urgency = analysis['urgency']
    price_range = f"${analysis['price_range'][0]} - ${analysis['price_range'][1]}"
    
    ai_summary = f"### AI Recommendation\n**Category:** {category} | **Urgency:** {urgency} | **Estimated Price:** {price_range}\n\n{analysis['message']}"
    
    # 2. Worker Recommendations
    workers = RecommendationEngine.get_recommended_workers(category)
    
    # Format workers for display
    worker_list = []
    for w in workers:
        worker_list.append([
            w['id'],
            w['name'],
            f"⭐ {w['avg_rating']} ({w['total_reviews']} reviews)",
            f"${w['base_price']}",
            f"{w['distance']} km",
            "Available" if w['available_slots'] > 0 else "Fully Booked"
        ])
        
    return ai_summary, worker_list

def create_search_tab():
    with gr.Tab("Search & AI Recommend"):
        gr.Markdown("## Find the Right Service Provider")
        
        with gr.Row():
            with gr.Column(scale=2):
                problem_input = gr.Textbox(
                    label="Describe your problem", 
                    placeholder="e.g., My AC is not cooling and making a loud noise...",
                    lines=3
                )
                search_btn = gr.Button("Analyze & Find Workers", variant="primary")
            
            with gr.Column(scale=3):
                ai_output = gr.Markdown("AI analysis will appear here after you describe your problem.")
        
        gr.Markdown("### Recommended Workers")
        worker_results = gr.Dataframe(
            headers=["ID", "Name", "Rating", "Base Price", "Distance", "Availability"],
            datatype=["number", "str", "str", "str", "str", "str"],
            interactive=False
        )
        
        search_btn.click(
            fn=search_workers,
            inputs=[problem_input],
            outputs=[ai_output, worker_results]
        )
        
    return problem_input, worker_results
