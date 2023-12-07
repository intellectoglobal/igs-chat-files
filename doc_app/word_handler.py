from langchain.document_loaders import Docx2txtLoader

class WordHandler:  
    def __init__(self, file):
        self.file = file

    def extract_word_content_to_document(self):
        try:
            with open(f"./input/{self.file.name}", 'wb') as f:
                f.write(self.file.read())
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except Exception as e:
            print(f"An error occurred on extract Word file: {str(e)}")
            return None

        name = self.file.name
        loader = Docx2txtLoader(f'./input/{name}')
        documents = loader.load()
        return documents
