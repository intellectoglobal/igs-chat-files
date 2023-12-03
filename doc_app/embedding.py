from langchain.vectorstores.pgvector import PGVector
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.openai import OpenAIEmbeddings
import os
from prompt import PromptTemplate
from openai import error as openai_error
import streamlit as st

class EmbeddingGenerator:

    def __init__(self, documents):
        self.documents = documents

    def generate_embeddings(self):
        # Split text into chunks
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=20,
            length_function=len
        )

        chunks = text_splitter.split_documents(self.documents)

        # # Alternatively, you can create it from environment variables.
        CONNECTION_STRING = PGVector.connection_string_from_db_params(
        driver=os.environ.get("PGVECTOR_DRIVER", "psycopg2"),
        host=os.environ.get("PGVECTOR_HOST", "localhost"),
        port=int(os.environ.get("PGVECTOR_PORT", "5434")),
        database=os.environ.get("PGVECTOR_DATABASE", "vector_db"),
        user=os.environ.get("PGVECTOR_USER", "postgres"),
        password=os.environ.get("PGVECTOR_PASSWORD", "12345"),
        )

        COLLECTION_NAME = "state_of_union_vectors"

        # Creating embeddings
        try:
            embeddings = OpenAIEmbeddings()
            db = PGVector.from_documents(
                embedding=embeddings,
                documents=chunks,
                collection_name=COLLECTION_NAME,
                connection_string=CONNECTION_STRING,
                )
            return db
        except openai_error.OpenAIError as e:
            if "Request too large" in str(e):
                st.error("Error: Request too large. Please reduce the file size.")
            else:
                st.error(f"OpenAIError: {str(e)}")
        

    def answer_question(self, user_question):
        # Similarity search
        db =self.generate_embeddings()
        docs = None
        if db is not None:
            docs = db.similarity_search(user_question)
            # Rest of your code...
        else:
            # Handle the case where db is None
            print("Failed to generate embeddings.")

        # Question answering
        llm = OpenAI()
        chain = load_qa_chain(llm, chain_type="stuff", prompt=PromptTemplate.PROMPT)
        response = chain.run(input_documents=docs, question=user_question)