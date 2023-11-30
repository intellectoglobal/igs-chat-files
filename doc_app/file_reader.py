from dotenv import load_dotenv
import os
import streamlit as st
from PyPDF2 import PdfReader
from langchain.document_loaders import PyPDFLoader
from langchain.docstore.document import Document
from embedding import EmbeddingGenerator
import langchain
from openai import error as openai_error


langchain.debug=True

class FileReaderApp:
    def __init__(self):
        load_dotenv()
        st.set_page_config(page_title="ASK YOUR PDF")
        st.header("ASK Your PDF")

        # Upload file
        self.pdf_file = st.file_uploader("Upload your PDF", type="pdf")

    def run(self):
        if self.pdf_file is not None:
            # pdf_reader = PdfReader(self.pdf_file)
            uploaded_file = self.pdf_file
            print(dir(uploaded_file))
            print(uploaded_file.name)
            # text = ""
            # for page in pdf_reader.pages:
            #     text += page.extract_text()

            def extract_pdf_content_to_text_file(uploaded_file):
                try:
                    # Create a BytesIO object to handle in-memory PDF content
                    with open(f"./input/{uploaded_file.name}", 'wb') as f:
                        f.write(uploaded_file.read())
                except Exception as e:
                    print(f"An error occurred on extract pdf: {str(e)}")
                return uploaded_file.name

            # Assuming you have 'pdf_content' variable containing the PDF content
            # Replace 'output.txt' with the desired path for the text output file
            # output_file_path = r'C:\Users\ranji\projects\doc_app\output.txt'

            # Convert PDF content to text file
            name = extract_pdf_content_to_text_file(uploaded_file)
            print(name)

            loader = PyPDFLoader(f'./input/{name}')
            documents = loader.load()

            print(documents)

            embedding = EmbeddingGenerator(documents)

            print(embedding)
                
            user_question = st.text_input("Ask a question about your file: ")
            if user_question:
                response = embedding.answer_question(user_question)
                st.write(response)
            

if __name__ == "__main__":
    app = FileReaderApp()
    app.run()
