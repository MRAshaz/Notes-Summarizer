import streamlit as st
from transformers import pipeline
import fitz


class NotesApp:
    def __init__(self):
        self._setup_ui()

    def _setup_ui(self):
        st.markdown(
            """
    <style>
    div.stButton > button:first-child {
        background-color: #0000FF;
        color:white;
    }
    div.stButton > button:first-child:hover {
        background-color: cyan;
        color:grey;
    }
    </style>
""",
            unsafe_allow_html=True,
        )
        # Header
        st.header("AI-Powered Note Summarizer")
        st.write(
            "Upload your notes or lecture slides (PDF) and  \nget a quick summary + flashcards!"
        )

        # File upload part
        st.divider()
        self.file = st.file_uploader("Upload PDF file", type="pdf")
        if self.file:
            st.success("File uploaded successfully ✔")
        st.divider()

        self.send_button = st.button(
            "Summarize notes", on_click=self.model, width="stretch"
        )

    def model(self):
        summarizer = pipeline("summarization", model="t5-small")
        # Using PyMuPDF to open the pdf and extract text
        if self.file:
            doc = fitz.open(stream=self.file.read(), filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()

            summary = summarizer(
                text[:1000], max_length=130, min_length=30, do_sample=False
            )
            st.subheader("📖 Summary")
            st.write(summary[0]["summary_text"])
        else:
            st.error("Please upload a PDF file first")


if __name__ == "__main__":
    NotesApp()
