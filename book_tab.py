import gradio as gr
from booking_service import BookingService
from database import get_db_connection

def get_worker_slots(worker_id):
    if not worker_id:
        return []
    slots = BookingService.get_available_slots(worker_id)
    return [(slot['id'], slot['slot_time']) for slot in slots]

def handle_booking(user_id, worker_id, slot_id, problem_description):
    if not user_id or not worker_id or not slot_id:
        return "Please select a worker and a time slot."
    
    success, message = BookingService.create_booking(user_id, worker_id, slot_id, problem_description)
    return message

def create_book_tab():
    with gr.Tab("Book Service"):
        gr.Markdown("## Book Your Service Appointment")
        
        with gr.Row():
            with gr.Column():
                user_id_input = gr.Number(label="Your User ID (Mock Login)", value=1, precision=0)
                worker_id_input = gr.Number(label="Worker ID (from Search)", precision=0)
                slot_dropdown = gr.Dropdown(label="Select Time Slot", choices=[])
                problem_desc = gr.Textbox(label="Problem Description", lines=2)
                
                refresh_slots_btn = gr.Button("Refresh Available Slots")
                book_btn = gr.Button("Confirm Booking", variant="primary")
                
            with gr.Column():
                booking_status = gr.Markdown("Select a worker and click 'Refresh' to see available slots.")
        
        def update_slots(worker_id):
            slots = get_worker_slots(worker_id)
            if not slots:
                return gr.update(choices=[], value=None), "No slots available for this worker."
            choices = [f"{s[1]} (ID: {s[0]})" for s in slots]
            return gr.update(choices=choices), f"Found {len(slots)} available slots."

        refresh_slots_btn.click(
            fn=update_slots,
            inputs=[worker_id_input],
            outputs=[slot_dropdown, booking_status]
        )
        
        def process_booking(user_id, worker_id, slot_str, problem):
            if not slot_str:
                return "Please select a slot."
            # Extract ID from "2026-03-20 10:00:00 (ID: 5)"
            slot_id = int(slot_str.split("ID: ")[1].replace(")", ""))
            return handle_booking(user_id, worker_id, slot_id, problem)

        book_btn.click(
            fn=process_booking,
            inputs=[user_id_input, worker_id_input, slot_dropdown, problem_desc],
            outputs=[booking_status]
        )
        
    return worker_id_input
