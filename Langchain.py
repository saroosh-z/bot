import os
from langchain.prompts import ChatPromptTemplate
from langchain import Cohere, PromptTemplate, chains, LLMChain

from langchain.chains import RetrievalQA
from langchain.embeddings import CohereEmbeddings
from langchain.vectorstores import Chroma

def answer_as_bot(question):
    template = """
    you are a chatbot who is to answer user questions. 
    Question: {question}
    """
    # template = question
    # prompt = PromptTemplate.from_template(template)

    prompt = PromptTemplate(template=template, input_variables=["question"])
    print("answer_as_chatbot prompt:", prompt)

    llm = Cohere(cohere_api_key=os.environ["COHERE_API_KEY"])

    llm_chain = LLMChain(prompt=prompt, llm=llm)
    print("::answer_as_chatbot running llm_chain")
    print("::answer_as_chatbot running llm_chain answer: ", llm_chain.run(question))
    return llm_chain.run(question)



def load_db():
    print("::Loading Chroma DB ")
    try:
        embeddings = CohereEmbeddings(cohere_api_key=os.environ["COHERE_API_KEY"])
        vectordb = Chroma(persist_directory='db', embedding_function=embeddings)
        qa = RetrievalQA.from_chain_type(
            llm=Cohere(cohere_api_key=os.environ["COHERE_API_KEY"]),
            chain_type="refine",
            retriever=vectordb.as_retriever(),
            return_source_documents=True
        )
        return qa
    except Exception as e:
        print("Error:", e)



