from langchain.document_loaders import UnstructuredExcelLoader

class ExcelHandler:
    
    def __init__(self, file):
        self.file = file

    def extract_excel_content_to_document(self):
        try:
            with open(f"./input/{self.file.name}", 'wb') as f:
                f.write(self.file.read())
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except Exception as e:
            print(f"An error occurred on extract Excel file: {str(e)}")
            return None  # or handle it as appropriate for your use case

        name = self.file.name
        loader = UnstructuredExcelLoader(f'./input/{self.file.name}', mode="elements")
        docs = loader.load()
        return docs
