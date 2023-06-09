from google_play_scraper import Sort, reviews, app
from tqdm import tqdm
import pandas as pd

app_infos = []
apps_id = ['br.com.brainweb.ifood', 'burgerking.com.br.appandroid']
app_reviews = []
app_reviews_2 = []
from main import generate_data_embeddings

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
    
    df_ifood = pd.read_csv("ifood_reviews.csv")
    print(df_ifood.head())
    
    df_content = df_ifood["content"]
    df_reduced_content = df_content.head(50)
    
    

