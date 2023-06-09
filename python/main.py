import openai
import pandas as pd
import weaviate
from openai.embeddings_utils import get_embedding
from google_play_scraper import Sort, reviews, app
from tqdm import tqdm
 
openai.api_key = "**"
client_weaviate = weaviate.Client("http://localhost:8080")

app_infos = []
apps_id = ['br.com.brainweb.ifood', 'burgerking.com.br.appandroid']
app_reviews = []
app_reviews_2 = []

def read_json_file():
    filename = "records.json"
    df = pd.read_json(filename)
    return df

def generate_data_embeddings(df):
    df['embedding'] = df['content'].apply(lambda row: get_embedding(row, engine="text-embedding-ada-002"))
    return df

def weaviate_create_schema():
    schema = {
        "classes": [{
            "class": "HistoryText",
            "description": "Contains the paragraphs of text along with their embeddings",
            "vectorizer": "none",
            "properties": [{
                "name": "content",
                "dataType": ["text"],
            }]
        }]
    }
    client_weaviate.schema.create(schema)
    
def weaviate_create_google_scraper_ifood_schema():
    schema_google_Scraper = {
        "classes": [{
            "class": "GoogleScraperIfoodContext",
            "description": "contem embeddings e dados de reclamações do ifood",
            "vectorizer": "none",
            "properties": [{
                "name": "content",
                "dataType": ["text"],
            }]
        }]
    }
    client_weaviate.schema.create(schema_google_Scraper)
    
def weaviate_add_data(df):
    client_weaviate.batch.configure(batch_size=10)
    with client_weaviate.batch as batch:
        for index, row in df.iterrows():
            text = row['text']
            ebd = row['embedding']
            batch_data = {
                "content": text
            }
            batch.add_data_object(data_object=batch_data, class_name="HistoryText", vector=ebd)

    print("Dado carregado")
    
def weaviate_add_data_ifood_review(df):
    client_weaviate.batch.configure(batch_size=10)
    with client_weaviate.batch as batch:
        for index, row in df.iterrows():
            text = row['content']
            ebd = row['embedding']
            batch_data = {
                "content": text
            }
            batch.add_data_object(data_object=batch_data, class_name="GoogleScraperIfoodContext", vector=ebd)

    print("Dado Ifood carregado")

def query( input_text, k):
    input_embedding = get_embedding(input_text, engine="text-embedding-ada-002")
    vec = {"vector": input_embedding}
    result = client_weaviate \
        .query.get("HistoryText", ["content", "_additional {certainty}"]) \
        .with_near_vector(vec) \
        .with_limit(k) \
        .do()

    output = []
    closest_paragraphs = result.get('data').get('Get').get('HistoryText')
    for p in closest_paragraphs:
        output.append(p.get('content'))

    return output

def query_ifood(input_text, k):
    input_embedding = get_embedding(input_text, engine="text-embedding-ada-002")
    vec = {"vector": input_embedding}
    result = client_weaviate \
        .query.get("GoogleScraperIfoodContext", ["content", "_additional {certainty}"]) \
        .with_near_vector(vec) \
        .with_limit(k) \
        .do()

    output = []
    closest_paragraphs = result.get('data').get('Get').get('GoogleScraperIfoodContext')
    for p in closest_paragraphs:
        output.append(p.get('content'))

    return output

def filter_ifood_reviews():
    
    for ap in tqdm(apps_id):
        for score in list(range(1,6)):
            for sort_order in [Sort.MOST_RELEVANT, Sort.NEWEST]:
                rvs, _ = reviews(
                    ap,
                    lang='pt',
                    country='br',
                    sort=sort_order,
                    count= 400 if score == 3 else 200,
                    filter_score_with=score
                )
                result, _ = reviews(
                        ap,
                        continuation_token=_
                        )

                for r in result:
                    r['sortOrder'] = 'most_relevant' if sort_order == Sort.MOST_RELEVANT else 'newest'
                    r['appId'] = ap
                app_reviews.extend(result)

                df = pd.DataFrame(app_reviews)
                df.to_csv("ifood_reviews.csv",sep=',')

if __name__ =='__main__':    
    
    #print("lendo dataframe")    
    #df_ifood = pd.read_csv("ifood_reviews.csv")      
    #df_content = df_ifood["content"]
    #df_reduced_content = df_content.head(50)    
    #print(df_ifood[["content"]].head(50))
    
    #dataframe = read_json_file()
    #dataframe = generate_data_embeddings(df_ifood[["content"]])
    #weaviate_create_google_scraper_ifood_schema()
    #weaviate_add_data_ifood_review(dataframe)
    
    input_text = "lixo de aplicativo"
    
    k_vectors = 5
    
    result = query_ifood(input_text, k_vectors)
    for text in result:
        print(text)
    
 #all_objects = client_weaviate.data_object.get(class_name="HistoryText")
#print(all_objects)
    
    