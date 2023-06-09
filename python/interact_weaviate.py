import weaviate
import openai
import json
from openai.embeddings_utils import get_embedding
import os 



openai.api_key = "**"

if __name__ == '__main__':
    #openai.api_key = "**"
    client = weaviate.Client("http://localhost:8080")
    #schemas = client_weaviate.data_object.get(class_name="LangChain_5043e227374b490bb6f088a971b725cb")
    #print(schemas) 
    #client = weaviate.Client(
    #url = "https://weaviate-bsruw8fa.weaviate.network",
    #auth_client_secret=weaviate.AuthApiKey(api_key="**"),  # Replace w/ your Weaviate instance API key
    #additional_headers = {
    #    "X-OpenAI-Api-Key": "**"  # Replace with your inference API key
    #})   
    
    #print(json.dumps((client.schema.get("LangChain_74bea6370f384a04b8427881a0285ade"))))
    #print(json.dumps(client.data_object.get()))
    
    #import json
    #print(json.dumps(len(client.data_object.get(class_name="LangChainDoc"))))
    
    print(client.query.aggregate("LangChainDoc").with_meta_count().do())
    print(client.query.get("LangChainDoc"))
   
    
   # input_text = "lima barreto"
   # input_embedding = get_embedding(text=input_text, engine="text-embedding-ada-002")
   # vec = {"vector":input_embedding}
   # result = client \
   #     .query.get("LangChain_74bea6370f384a04b8427881a0285ade", ["text","_additional {certainty}"]) \
   #     .with_near_vector(vec) \
   #     .with_limit(1) \
   #     .do()
   # 
   #
   # output = []
   # closest_paragraphs = result.get('data').get('Get').get('LangChain_74bea6370f384a04b8427881a0285ade')
   # for p in closest_paragraphs:
   #     output.append(p.get('text'))
#
   # print(output)