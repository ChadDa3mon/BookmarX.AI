import gradio as gr
from utils import search_db,get_markdown

with gr.Blocks() as demo:
    gr.Markdown("# Lynx\n\n[GitHub](https://github.com/ChadDa3mon/lynx/tree/main)") 
    with gr.Tab("Add Bookmark"):
        with gr.Row():
            add_url = gr.Textbox(label="URL To Add",info="Enter the URL you wish to add",scale=5)
    with gr.Tab("Search Bookmarks"):
        with gr.Row():
            search_term = gr.Textbox(label="Search Term")
        with gr.Row():
            search_results = gr.Dataframe(label="Search Results",headers=['URL','Summary'],wrap=True)
        with gr.Row():
            webpage_markdown = gr.Markdown()
        search_term.submit(search_db,search_term,search_results)
        search_results.select(get_markdown,search_results,webpage_markdown)


demo.launch(inbrowser=False,server_name="0.0.0.0")