from unstructured.partition.pdf import partition_pdf
import textwrap
import weaviate
from pathlib import Path
from AbstractExtractor import AbstractExtractor
from langchain.vectorstores.weaviate import Weaviate
from langchain.llms import OpenAI
from langchain.chains import ChatVectorDBChain

def getClient():    
    client = weaviate.Client(
        url = "https://weaviate-bsruw8fa.weaviate.network",
        auth_client_secret=weaviate.AuthApiKey(api_key="**"),  # Replace w/ your Weaviate instance API key
        additional_headers = {
            "X-OpenAI-Api-Key": "**"  # Replace with your inference API key
        })
    return client

def deleteSchemas(client):
    client.schema.delete_all()

def createSchema(client):
    schema = {
    "class": "Document",
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


    
if __name__  == '__main__':
    client = getClient()
#    
#    deleteSchemas(client)
#    
#    createSchema(client)
#    
#    data_folder = "/home/ekstein/kind/data"
#
#    data_objects = []
#
#    for path in Path(data_folder).iterdir():
#        if path.suffix != ".pdf":
#            continue
#
#    elements = partition_pdf(filename=path)    
#    
#    data_objects.append(elements)
#    
#    i = 0
#    client.batch.configure(batch_size=1000)
#    with client.batch as batch:
#        for data_object in data_objects:
#            for object in data_object:
#                i +=1
#                text = object.text
#                source = i
#                batch_data = {
#                    "textchunk":text,
#                    "source":str(i)
#                }
#                batch.add_data_object(data_object=batch_data, class_name="Document")
#                
#            
#    
#    prompt = """
#    quem é a Contratante ?
#
#{textchunk}
#
#"""      
#
#results = (
#    client.query.get("Document", "textchunk").with_generate(single_prompt=prompt).do()
#)  
#
#
#docs = results
#print(results)


client = weaviate.Client(
    url = "https://weaviate-bsruw8fa.weaviate.network",
    auth_client_secret=weaviate.AuthApiKey(api_key="**"),  # Replace w/ your Weaviate instance API key
    additional_headers = {
        "X-OpenAI-Api-Key": "**"  # Replace with your inference API key
    })

vectorstore = Weaviate(client, "Document", "textchunk")

MyOpenAI = OpenAI(temperature=0.0,
    openai_api_key="**")

qa = ChatVectorDBChain.from_llm(MyOpenAI, vectorstore)


chat_history = []

while True:
    print("faça uma pergunta sobre o contrato ")
    query = input("")
    result = qa({"question": query, "chat_history": chat_history})
    print(result["answer"])
    chat_history = [(query, result["answer"])]
            

    