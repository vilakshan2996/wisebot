from secret_key import openapi_key
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
import os
import streamlit as st
os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

# Embed and store the texts
# Supplying a persist_directory will store the embeddings on disk
persist_directory = '../db'

## here we are using OpenAI embeddings but in future we will swap out to local embeddings
embedding = OpenAIEmbeddings()
qa_chain = None
def loadData(collection_name):
    global qa_chain
    print("..............Loading data to vector DB...................",collection_name)
    # Now we can load the persisted database from disk, and use it as normal. 
    vectordb = Chroma(persist_directory=persist_directory, 
                    embedding_function=embedding,collection_name=collection_name)


    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    # create the chain to answer questions 
    qa_chain =  ConversationalRetrievalChain.from_llm(
            ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
            retriever,
            condense_question_llm=ChatOpenAI(model_name="gpt-3.5-turbo"),
            verbose=True,
        )

def execute_qa(input,chat_history):
    # Execute qa_chain with the query
    llm_response = qa_chain({ "question": input,
                "chat_history":chat_history ,})
    return llm_response['answer']

