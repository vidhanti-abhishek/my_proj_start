import gradio as gr
from booking_service import BookingService
from review_service import ReviewService

def get_user_bookings_view(user_id):
    if not user_id:
        return []
    bookings = BookingService.get_user_bookings(user_id)
    return [[b['id'], b['worker_name'], b['category'], b['status'], b['slot_time']] for b in bookings]

def submit_review(booking_id, user_id, worker_id, rating, comment):
    if not booking_id or not rating:
        return "Please provide a booking ID and rating."
    success, message = ReviewService.add_review(booking_id, user_id, worker_id, rating, comment)
    return message

def create_account_tab():
    with gr.Tab("My Account"):
        gr.Markdown("## Your Bookings & Reviews")
        
        user_id_input = gr.Number(label="Your User ID", value=1, precision=0)
        refresh_btn = gr.Button("Refresh My Bookings")
        
        bookings_table = gr.Dataframe(
            headers=["Booking ID", "Worker", "Category", "Status", "Time"],
            datatype=["number", "str", "str", "str", "str"],
            interactive=False
        )
        
        gr.Markdown("### Leave a Review")
        with gr.Row():
            with gr.Column():
                booking_id_input = gr.Number(label="Booking ID", precision=0)
                worker_id_input = gr.Number(label="Worker ID", precision=0)
                rating_input = gr.Slider(minimum=1, maximum=5, step=1, label="Rating (1-5)")
                comment_input = gr.Textbox(label="Review Comment", lines=2)
                review_btn = gr.Button("Submit Review", variant="primary")
            
            with gr.Column():
                review_status = gr.Markdown("Reviews can only be left for 'Completed' bookings.")
        
        refresh_btn.click(
            fn=get_user_bookings_view,
            inputs=[user_id_input],
            outputs=[bookings_table]
        )
        
        review_btn.click(
            fn=submit_review,
            inputs=[booking_id_input, user_id_input, worker_id_input, rating_input, comment_input],
            outputs=[review_status]
        )
        
    return user_id_input
