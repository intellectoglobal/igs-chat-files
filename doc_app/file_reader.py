from langchain.llms import OpenAI
from prompt import PROMPT
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
import streamlit as st
from langchain.vectorstores.pgvector import PGVector
from pdf_handler import PDFHandler
from excel_handler import ExcelHandler
from word_handler import WordHandler
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
import db_connection
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferMemory
import langchain
from openai import error as openai_error
from Error_handling import UnsupportedFileTypeError
from stream_handler import StreamHandler

langchain.debug = True


class FileReaderApp:
    st.set_page_config(page_title="IGS", page_icon="https://intellecto.co.in/wp-content/uploads/2019/06/110x110.png")
    st.title("IGS: Chat Files Genie")
    button_css =""".stButton>button {
        color: #EEF5FF;
        border-radius: 50%;
        height: 2em;
        width: 2em;
        font-size: 4px;
    }"""
    st.markdown(f'<style>{button_css}</style>', unsafe_allow_html=True)

    load_dotenv()

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    text_splitter = CharacterTextSplitter(
                separator="\n",
                chunk_size=1000,
                chunk_overlap=20,
                length_function=len
            )
    embeddings = OpenAIEmbeddings()
    
    allowed_file_types = ["pdf", "xlsx", "docx"]

    #Getting a uploaded file from user
    uploaded_file = st.file_uploader("Upload your file", type=allowed_file_types)

    # To notify file is loading
    with st.spinner('loading......'):
        try:
            #Checking the file Formate
            if uploaded_file is not None:
                collection_name = uploaded_file.name

                if uploaded_file.type == "application/pdf":
                    pdf_handler = PDFHandler(uploaded_file)
                    documents  =  pdf_handler.extract_pdf_content_to_document()
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                    print("i am excel")
                    excel_handler = ExcelHandler(uploaded_file)
                    documents  = excel_handler.extract_excel_content_to_document()
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    print("i am word")
                    word_handler = WordHandler(uploaded_file)
                    documents  =word_handler.extract_word_content_to_document()
        except UnsupportedFileTypeError as e:
            st.error(f"Unsupported file format: {uploaded_file.type}")

    # Clear chat if user cancels the uploaded file
    if uploaded_file is None:
        st.session_state['messages'] = []

    #looping the messages
    for msg in st.session_state["messages"]:
        if isinstance(msg, HumanMessage):
            st.chat_message("user").write(msg.content)
        else:
            st.chat_message("assistant").write(msg.content)
        
    if uploaded_file is not None:
        try:
            if prompt := st.chat_input("Enter your question here!"):
                st.chat_message("user").write(prompt)
                with st.chat_message("assistant"):
                    stream_handler = StreamHandler(st.empty())
                    llm = OpenAI(streaming=True, callbacks=[stream_handler])
                    chain = load_qa_chain(llm, chain_type="stuff", prompt=PROMPT)

                    # msg_placeholder = st.empty()
                    chunks = text_splitter.split_documents(documents)
                    db = PGVector.from_documents(
                                                embedding=embeddings,
                                                documents=chunks,
                                                collection_name=collection_name,
                                                connection_string=db_connection.CONNECTION_STRING,
                                            )
                    docs = db.similarity_search(prompt)
                    response = chain.run(input_documents=docs, question=prompt)

                    st.session_state.messages.append(HumanMessage(content=prompt))
                    st.session_state.messages.append(AIMessage(content=response))
        except openai_error.AuthenticationError as auth_error:
            st.error(f"Authentication error: {str(auth_error)}")
        except openai_error.RateLimitError as rate_limit_error:
            st.error(f"Rate limit exceeded: {str(rate_limit_error)}")
        except openai_error.APIError as api_error:
            st.error(f"OpenAI API error: {str(api_error)}")
        except Exception as generic_error:
            st.error(f"An unexpected error occurred: {str(generic_error)}")
                # msg_placeholder.markdown(response)

if __name__ == "__main__":
    FileReaderApp()