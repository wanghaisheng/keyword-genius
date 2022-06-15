from google_play_scraper import Sort, reviews_all
from app_store_scraper import AppStore
from google_play_scraper import app
import csv
from pathlib import Path
import pandas as pd
import random
import os
try:
    google_app_package_url = os.getenv('google_app_package_url').strip()
    if 'https://play.google.com/store/apps/details?id=' in google_app_package_url:
        
        google_app_package_name=google_app_package_url.replace('https://play.google.com/store/apps/details?id=','')
        # https://play.google.com/store/apps/details?id=com.twitter.android
        if not len(google_app_package_name.split('.'))==3:
            print('not support package,',google_app_package_url,google_app_package_name)
except:
    google_app_package_name='com.lemon.lvoverseas'
try:
# https://apps.apple.com/us/app/indycar/id606905722
#     https://apps.apple.com/us/app/capcut-video-editor/id1500855883
    apple_app_package_url = os.getenv('apple_app_package_url').strip()
    if 'https://apps.apple.com/us/app/' in apple_app_package_url:
        apple_app_package_name=apple_app_package_url.replace('https://apps.apple.com/us/app/','')
        apple_app_package_name=apple_app_package_name.split('/')[0]
        if not len(apple_app_package_name)>0:
            print('not support package,',apple_app_package_url,apple_app_package_name)        
except:
    apple_app_package_name='capcut-video-editor'
try:
    country=os.getenv('country')
except:
    country='us'
try:
    lang=os.getenv('lang')
except:
    lang='en'
OUTPUT_DIR = Path("data")


googlerows = []
def play_store_scraper(package):
    results = reviews_all(package,sleep_milliseconds=0,lang='en',country='us',sort=Sort.MOST_RELEVANT)


    # Adds the fields to the CSV
    for x, item in enumerate(results):
        googlerows.append(item)

    

    df = pd.DataFrame(googlerows)
    df.to_csv("./"+package+'-'+lang+'-'+country+'-'+"google-app-review.csv", index=False)

applerows = []

def app_store_scraper(app_name,country="us",lang='en'):
    app = AppStore(country=country,app_name=app_name)
    app.review(sleep = random.randint(3,6))
#     app.review()

    for review in app.reviews:
        data={}
        data['score']= review['rating']
        data['userName']= review['userName']
        data['review']= review['review'].replace('\r',' ').replace('\n',' ')
        
        applerows.append(data)
    df = pd.DataFrame(applerows)
    df.to_csv("./"+app_name+'-'+lang+'-'+country+'-'+"apple-app-review.csv", index=False)
def app_reviews(country_code,app_id):

    return "https://itunes.apple.com/%s/rss/customerreviews/id=%s/sortBy=mostRecent/json" % (country_code, app_id)    
# https://itunes.apple.com/us/rss/customerreviews/id=1500855883/sortBy=mostRecent/json    
if not os.getenv('google_app_package_url')=='':
    play_store_scraper(google_app_package_name)
if not os.getenv('apple_app_package_name')=='':
    app_store_scraper(apple_app_package_name)

#huawei  xiaomi samsung

