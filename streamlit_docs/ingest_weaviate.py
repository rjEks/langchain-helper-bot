import weaviate
from langchain.vectorstores.weaviate import Weaviate
from langchain.document_loaders import ReadTheDocsLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Weaviate



def getClient():    
    client = weaviate.Client("http://localhost:8080",timeout_config=(5,600))
    return client

def deleteSchemas(client):
    client.schema.delete_all()

def createSchema(client):
    schema = {
    "class": "LangChainDoc",
    "vectorizer": "text2vec-openai",
    "properties": [
        {
            "name": "source",
            "dataType": ["text"],
        },
        {
            "name": "textchunk",
            "dataType": ["text"],
            "moduleConfig": {
                "text2vec-openai": {"skip": False, "vectorizePropertyName": False}
            },
        },
    ],
    "moduleConfig": {
        "generative-openai": {},
        "text2vec-openai": {"model": "ada", "modelVersion": "002", "type": "text"},
    },
}
    client.schema.create_class(schema)
    
def ingest_docs():
             
    loader = ReadTheDocsLoader(path="/home/ekstein/kind/data/langchain-docs/python.langchain.com/en/latest")
    raw_documents = loader.load()        
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100, separators=["\n\n", "\n", " ", ""])
    documents = text_splitter.split_documents(documents=raw_documents)
    print(f"dividido em {len(documents)} chunks ")
    
    for doc in documents:
        old_path = doc.metadata["source"] 
        new_url = old_path.replace("langchain-docs","https:/")
        doc.metadata.update({"source":new_url})
        
    print(f"inserindo {len(documents)} no Weaviate")
    embeddings = OpenAIEmbeddings(openai_api_key="**")
    
    client = getClient()
    
    vectorstore = Weaviate(client,"LangChainDoc","text_content")
    
    vectorstore.from_documents(documents=documents,embedding=embeddings,weaviate_url="http://localhost:8080",index_name="LangChainDoc")
        
if __name__=='__main__':
        #obtendo conexao
        client = getClient()
        
        #deleteSchemas(client)
        
        #createSchema(client)
        
        ingest_docs(client)
        
        