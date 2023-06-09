import os

from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Weaviate
from langchain import VectorDBQA, OpenAI
import weaviate


client = weaviate.Client("http://localhost:8080")

vectorstore = Weaviate(client, "PodClip", "content")

if __name__ == "__main__":
    print("Hello VectorStore!")
    loader = TextLoader("mediumblog1.txt")
    document = loader.load()
    
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(document)
    
    embeddings = OpenAIEmbeddings(openai_api_key="**")

    db = Weaviate.from_documents(texts, embeddings, weaviate_url="http://localhost:8080", by_text=False)
    
    qa = VectorDBQA.from_chain_type(
        llm=OpenAI(openai_api_key="**"), chain_type="stuff", vectorstore=db, return_source_documents=False
    )
        
    query = "What is a vector DB? Give me a 5 word answer for a begginner"
    #docs = db.similarity_search(query)
    result = qa({"query": query})
    print(result["result"])
