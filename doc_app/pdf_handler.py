from langchain.document_loaders import PyPDFLoader
from langchain.docstore.document import Document

class PDFHandler:
        
        def __init__(self, file):
            self.file = file

        def extract_pdf_content_to_document(self):
                file = self.file
                try:
                    with open(f"./input/{file.name}", 'wb') as f:
                        f.write(file.read())
                except FileNotFoundError as e:
                    print(f"File not found: {e}")
                except Exception as e:
                    print(f"An error occurred on extract pdf: {str(e)}")
                name=file.name
                loader = PyPDFLoader(f'./input/{name}')
                documents = loader.load()
                return documents

