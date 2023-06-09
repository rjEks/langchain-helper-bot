import os

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.vectorstores import Weaviate
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import getpass

import weaviate


WEAVIATE_URL  = "https://weaviate-bsruw8fa.weaviate.network"
os.environ["WEAVIATE_API_KEY"] = "**"

client = weaviate.Client(
    url = "https://weaviate-bsruw8fa.weaviate.network",
    auth_client_secret=weaviate.AuthApiKey(api_key=""),  # Replace w/ your Weaviate instance API key
    additional_headers = {
        "X-OpenAI-Api-Key": "**"  # Replace with your inference API key
    })

if __name__ == "__main__":
    #Livro Mec Contos do Lima Barreto
    pdf_path = "bv000155.pdf"
    
    #Importando document Loader
    loader = PyPDFLoader(file_path=pdf_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(
        chunk_size=1000, chunk_overlap=30, separator="\n"
    )
    
    #Splitando Documentos
    docs = text_splitter.split_documents(documents=documents)

    embeddings = OpenAIEmbeddings(openai_api_key="**")
    
    db = Weaviate.from_documents(docs, embeddings, weaviate_url=WEAVIATE_URL, by_text=False)
   
    qa = RetrievalQA.from_chain_type(
         llm=OpenAI(openai_api_key="**"), chain_type="stuff", retriever=db.as_retriever()
    )
    
             
    res = qa.run("Quem é Fabricio ? ")
    print(res)
