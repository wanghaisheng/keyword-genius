# POST /search/keywords/google/metrics
# 	https://keywordtool.io/search/keywords/youtube/metrics?signature=ac32cb4482b8bc71efd92906562e1a3b594ad35b6fc271116331b6e2a0ada0c6
# Accept
# 	application/json, text/plain, */*
# Accept-Encoding
# 	gzip, deflate, br
# Accept-Language
# 	en-US,en;q=0.5
# Connection
# 	keep-alive
# Content-Length
# 	167
# Content-Type
# 	application/json
import requests
import base64
import os
import time
from traceback import print_exc
import random
import json
from time import sleep
from requests.exceptions import Timeout

def get(keyword):
    
    try: 
        headers = {
#             'authority': 'translate.volcengine.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            # 'origin': 'chrome-extension://jmnhemdajboodicneejdlpanmijclhef',
            'accept-encoding': 'gzip, deflate, br',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'none',
            # 'cookie':'x-jupiter-uuid=1685206167481291; i18next=zh-CN; s_v_web_id=verify_li6888fu_E2yIFhRA_Amo7_42lt_93A0_OrjFArSkTope; ttcid=29381a8ff7874daea9f91f7bb6a91c4b41; isIntranet=-1; ve_doc_history=4640; tt_scid=QmoChhEFFYvYA9lNkQwiGu8VOuOiJDyGbcNg7Ysc9h4O-ceoZRVLq0cw5H4qbVSl79af; __tea_cache_tokens_3569={"web_id":"7237905415249118780","user_unique_id":"7237905415249118780","timestamp":1685208803602,"_type_":"default"}; referrer_title=音视频文件翻译API--机器翻译-火山引擎',
            'content-type':'application/json; charset=UTF-8',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.51',

        }

        json_data = {"filter_keywords":"","filter_keywords_partial_match":"","negative_keywords":"","keywords_payload":"6d924c0a1cce3a3bc4aae32d81a821f6","sort":"keywordsAsc","total":100}
        data=json.dumps(json_data)
        # json serializes Python dictionaries to JSON. data takes arbitrary bytes.

        max_retries = 3
        timeout = 15

        retry_count = 0
        while retry_count < max_retries:
            try:
                
                fname=keyword.strip()
                
                if not os.path.exists('./results/'+fname+'.json'):
                    print('file is not yet :','./results/'+fname+'.json')      
                    sleep_time = random.uniform(1,3)
                    print(f"Sleeping for {sleep_time} seconds...")
                    time.sleep(sleep_time)                              
                    response = requests.post('https://keywordtool.io/search/keywords/youtube/metrics',  headers=headers, json= json_data,proxies={'http':None,'https':None}, timeout=timeout)
                    
                    
                    response.raise_for_status()
                    print('Request successful!')
                    # print('Response:', response.text)
                    try:
                        result=response.json()['all_keywords']          

                        
                        with open('./results/'+fname+'.json','wb') as ff:
                            ff.write(result)
                    except:
                        print('response content has no audio data filed',response.text)
                        retry_count += 1
                        with open('./combines/failed.txt','a+') as ff:
                            ff.write(voice+"\n")
                        break
                                
                return ('./results/'+fname+'.json')                
                break
            except Timeout:
                print('Request timed out. Retrying...')
                retry_count += 1
            except requests.RequestException as e:
                print('An error occurred:', e)
                break

        if retry_count == max_retries:
            print('Maximum number of retries reached.')


        
    except:
        print_exc()
        return None
get("capcut")
