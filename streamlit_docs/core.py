import weaviate
from langchain.vectorstores.weaviate import Weaviate
from langchain.document_loaders import ReadTheDocsLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Weaviate
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA, ConversationalRetrievalChain


def getClient():    
    client = weaviate.Client("http://localhost:8080",timeout_config=(5,600))
    return client

def run_llm(query,chat_history):
    client = weaviate.Client("http://localhost:8080",timeout_config=(5,600))
    
    embeddings = OpenAIEmbeddings(openai_api_key="**")
     
    docsearch = Weaviate(client,"LangChainDoc","text",embeddings, attributes=["source,text"], by_text=False)
     
    chat = ChatOpenAI(openai_api_key="**", verbose=True,temperature=0)
     
    #qa = RetrievalQA.from_chain_type(llm=chat, chain_type="stuff", retriever=docsearch.as_retriever(), return_source_documents=True)
    
    qa = ConversationalRetrievalChain.from_llm(llm=chat, retriever=docsearch.as_retriever(), return_source_documents=True)

    return qa({"question":query, "chat_history":chat_history})
    
if __name__=='__main__':
        #obtendo conexao
        #client = getClient()
        print(run_llm("Wha is RetrievalQA chain ? Answer in portuguese"))
            