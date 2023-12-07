from langchain.prompts import PromptTemplate

prompt_template = """You are an expert in answering a question by using the following pieces of context If you don't know the answer, just say that there is no content regarding to this question from the provided file and gentle give some other suggestion. don't try to make up an answer
{context}

Question: {question}
Helpful Answer:"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)