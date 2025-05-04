from unicodedata import category
import requests  # Include functionality to make a call to the remote websites
import pandas as pd
import re
import wordninja

import os
import random
import time

#原理初步设想为，假设关键词为jewelry,在instagram中输入"#jewelry",从搜索框的下拉推荐列表中获取扩展关键词
#instagram tag都有一个volume在 但其他的我暂时没想好怎么获取
urls = {
    "google": "https://suggestqueries.google.com/complete/search?client=chrome&q=",
    "amazon": "https://completion.amazon.com/search/complete?search-alias=aps&client=amazon-search-ui&mkt=1&q=",
    "youtube": "http://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q=",
    "etsy":"https://www.etsy.com/suggestions_ajax.php?extras={&quot;expt&quot;:&quot;off&quot;,&quot;lang&quot;:&quot;en-GB&quot;,&quot;extras&quot;:[]}&version=10_12672349415_19&search_type=all&search_query=",
    "instagram":"https://www.instagram.com/web/search/topsearch/?context=blended&include_reel=true&query=%23",
    "tiktok":"https://www.tiktok.com/api/search/general/preview/?aid=1988&app_language=en&app_name=tiktok_web&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0 (Windows)&channel=tiktok_web&cookie_enabled=true&device_id=7034896245308212741&device_platform=web_pc&focus_state=true&from_page=search&history_len=17&is_fullscreen=false&is_page_visible=true&os=windows&priority_region=&referer=&region=KR&screen_height=840&screen_width=1344&tz_name=Asia/Shanghai&webcast_language=en&keyword="
}


proxies = {
	'http': 'socks5://127.0.0.1:1080',
	'https': 'socks5://127.0.0.1:1080'
}

def url_ok(url):


    try:
        response = requests.head(url)
    except Exception as e:
        # print(f"NOT OK: {str(e)}")
        return False
    else:
        if response.status_code == 200:
            # print("OK")
            return True
        else:
            print(f"NOT OK: HTTP response code {response.status_code}")

            return False

def rep(m):
    s=m.group(1)
    return ' '.join(re.split(r'(?=[A-Z])', s))

def get_longtail_keywords_from_recommend(keyword_inputfilename,keyword_outputfilename,depth=0):
    df_queries = pd.read_csv(keyword_inputfilename)
    # root.csv will look like below
    # keywords (header)
    # jewelry
    # kids school
    # search engine optimization

    queries = df_queries.keywords

    to_be_saved_queries = []
    all_autosuggestions = []
    domains = []
    for query in queries:
        for (domain, url) in urls.items():
 
            print('process',domain,'keyword',query)
           # add the query to the url
            remote_url = url + query
            # print(f"Remote url : {remote_url}")
            headers = {'User-Agent': 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'}

            response=''
            if url_ok('http://www.google.com'):
                # print('network is fine,there is no need for proxy ')
                response = requests.get(remote_url).json()

            else:
                # print('google can not be access ')

                # print('we need for proxy ',proxies)            
                response = requests.get(remote_url,proxies=proxies).json()
            # print(response)
            auto_suggest=[]
            if domain=='etsy':
                for item in response['results']:
                    if "</span>" in item['query']:
                        pass
                    else:
                        if query==item['query']:
                            pass
                        else:                        
                            auto_suggest.append(item['query'])
            elif domain in ['google','youtube','amazon']:
                if query in response[1]:
                   response[1].remove(query)
                auto_suggest = response[1]
                # print(response[1])
            elif domain =='tiktok':
                # print(response)
                for item in response['sug_list']:
                    # print(item['content'])
                    if query==item['content']:
                        pass
                    else:
                        auto_suggest.append(item['content'])     
            elif domain=='instagram':
                for item in response['hashtags']:
                    k = ' '.join(wordninja.split(item['hashtag']['name']))
                    if query==k:
                        pass
                    else:                    
                        auto_suggest.append(k)       
                    item['hashtag']['media_count']     
            # print(auto_suggest)
            auto_suggest = [ii for n,ii in enumerate(auto_suggest) if ii not in auto_suggest[:n]]            
            for suggestion in auto_suggest:
                to_be_saved_queries.append(query)
                all_autosuggestions.append(suggestion)
                domains.append(domain)
            time.sleep(random.randint(3, 10))

        
        df = pd.DataFrame({"domain": domains, "query": to_be_saved_queries, "keywords": all_autosuggestions})
        df.to_csv(keyword_outputfilename,  mode='a', index=False)
async def get_longtail_keywords_from_one(query,platforms):
    # root.csv will look like below
    # keywords (header)
    # jewelry
    # kids school
    # search engine optimization
    temp_urls=[]
    for p in platforms:
        temp_urls.append(urls[p])

    to_be_saved_queries = []
    all_autosuggestions = []
    domains = []
    for (domain, url) in temp_urls:

        print('process',domain,'keyword',query)
        # add the query to the url
        remote_url = url + query
        # print(f"Remote url : {remote_url}")
        headers = {'User-Agent': 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'}

        response=''
        if url_ok('http://www.google.com'):
            # print('network is fine,there is no need for proxy ')
            response = requests.get(remote_url).json()

        else:
            # print('google can not be access ')

            # print('we need for proxy ',proxies)            
            response = requests.get(remote_url,proxies=proxies).json()
        # print(response)
        auto_suggest=[]
        if domain=='etsy':
            for item in response['results']:
                if "</span>" in item['query']:
                    pass
                else:
                    if query==item['query']:
                        pass
                    else:                        
                        auto_suggest.append(item['query'])
        elif domain in ['google','youtube','amazon']:
            if query in response[1]:
                response[1].remove(query)
            auto_suggest = response[1]
            # print(response[1])
        elif domain =='tiktok':
            # print(response)
            for item in response['sug_list']:
                # print(item['content'])
                if query==item['content']:
                    pass
                else:
                    auto_suggest.append(item['content'])     
        elif domain=='instagram':
            for item in response['hashtags']:
                k = ' '.join(wordninja.split(item['hashtag']['name']))
                if query==k:
                    pass
                else:                    
                    auto_suggest.append(k)       
                item['hashtag']['media_count']     
        # print(auto_suggest)
        auto_suggest = [ii for n,ii in enumerate(auto_suggest) if ii not in auto_suggest[:n]]            
        for suggestion in auto_suggest:
            to_be_saved_queries.append(query)
            all_autosuggestions.append(suggestion)
            domains.append(domain)
        time.sleep(random.randint(3, 10))

    
    # df = pd.DataFrame({"domain": domains, "query": to_be_saved_queries, "keywords": all_autosuggestions})
    # df.to_csv(outputfilename,  mode='a', index=False)
    return all_autosuggestions
if __name__ == "__main__":
        
    for root, dirs, files in os.walk('.'):
        for name in files:
            if name.endswith('-lv0.csv'):
                category=name.split('-')[0]
                print('========',category)
        # 		category='jewelry'
                category_root_keyword=category+'-lv0.csv'
                category_level_1_keyword=category+'-lv1.csv'
                category_level_2_keyword=category+'-lv2.csv'
                category_level_3_keyword=category+'-lv3.csv'
                category_level_4_keyword=category+'-lv4.csv'
                category_level_5_keyword=category+'-lv5.csv'

                get_longtail_keywords_from_recommend(category_root_keyword,category_level_1_keyword)
                get_longtail_keywords_from_recommend(category_level_1_keyword,category_level_2_keyword)
                get_longtail_keywords_from_recommend(category_level_2_keyword,category_level_3_keyword)
                get_longtail_keywords_from_recommend(category_level_3_keyword,category_level_4_keyword)
                get_longtail_keywords_from_recommend(category_level_4_keyword,category_level_5_keyword)



