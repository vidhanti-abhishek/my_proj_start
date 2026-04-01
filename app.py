import gradio as gr 
import os
import sys

# Add the project root to sys.path so root modules can be imported directly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import init_db
from search_tab import create_search_tab
from book_tab import create_book_tab
from account_tab import create_account_tab

def main():
    # Initialize database
    init_db()
    
    # Create Gradio interface
    with gr.Blocks(title="FixItGo - AI Service Booking Platform") as demo:
        gr.Markdown("# 🛠️ FixItGo")
        gr.Markdown("### Your AI-Powered Service Booking Platform")
        
        with gr.Tabs():
            # Create tabs and get relevant inputs/outputs for cross-tab interaction
            search_input, search_results = create_search_tab()
            worker_id_input = create_book_tab()
            user_id_input = create_account_tab()
            
        gr.Markdown("---")
        gr.Markdown("© 2026 FixItGo - Production Ready AI Service Platform")
        
    return demo

if __name__ == "__main__":
    demo = main()
    demo.launch(server_name="0.0.0.0", server_port=7860)
