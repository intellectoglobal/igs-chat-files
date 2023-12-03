from langchain.prompts import PromptTemplate

class PromptTemplate:
    prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that there is no content regarding to this question from the provided file, don't try to make up an answer.
    {context}
    Question: {question}
    Helpful Answer:"""
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )