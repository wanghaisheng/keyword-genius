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

def get(keywords):
    
    try: 
        
        headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
'Accept':'application/json, text/plain, */*',
'Accept-Language':'en-US,en;q=0.5',
'Accept-Encoding':'gzip, deflate, br',
'X-Requested-With':'XMLHttpRequest',
'Content-Type':'application/json',
'Token':'eyJpdiI6Ik94Y3doRjFmN2lHbmo2blhjVk9vekE9PSIsInZhbHVlIjoiUS93UGV2R05pRFdhczIxVEF0ZnhKZXlEVnNIc09MSXRnRUtkc2ZRaDVEeHFDamZkMnZNOE9hUHFIZ2lLM1RvOXJsZ08vY2toRWxHTWlKSXl5S0R3bldZM3E3Ykc5RVF3WFRxOEN5YTQwbUhvdGdjaTFjQU9seTRiVmlaV1c2SEI1L0NLbXJ3M2dOb1VrYm54ekgvMmNmUU9qTVdqYVNSTnVaY2FUVFc4Y1RmdFhKYXJGTHpnaExUaUM0ZkFKek5NVGo1dGJ5bjEyY3ZqM05SSnlyTjJNTHY2TUZtWjZ5SXFoYWpVMGc0UW5BZkgvOXNiQ1B0L3JURVQ2alQ0MTlGQkZpaGNsLzduRU54U2E4N1YybFZtYmJUSk5UWUxMMTNEM1VnVW8xQVEraGw1TmpJcGI4Y1hxQ3Y1WjRpQnJ3d0tLQzhXY3VETmVNQnFlSEVYMlpRd0ZQRUM4am5mL0dpV09xUnNDa0d2UFVpd0k2QklNWGp0MWhZYTl1a005bDA4YkhLQ3ZRcWV5eGJuQ0NHY21PcjF0VU9XN0xyRkcxY2tPckg0c1NvbVRRRGtUYmNPbW5jYkNSa0VKTDdSVGU4ZmdLMTB1c3lDMFNVODdoU0p5YWZDMmFrVFk4VHlNSzgvR1YyUTNldmVaTWV4LzgydFNnMFZyMG1OQjRnemU5TlVoNVhoWHhITGxKNHlXalRhV0xFLzNIVmQ0cE9vakZDSlhxT0dLVEMvYnRGa1cwZ0RwQXYvUEtYTW4wbmd6L1lpS3UzTXdGVVpTZzF0KzlaQnpPaHdZaWRVZm5pTDAzTVJzNEV4OUdtNmV4Y2JPSkZ5K1VRS1FBQ0kzd1FUa3hTT1VCTmJsOGtmajl1NUQ4OVZ0WWRXdGNMbXI4UG1NaFhtcG9ucE55T1RubGRBWFp0RS9QbFppTG5PVHljYzdJcUR6YUpFVE5EdlhaalYwZW4wTzYxUXNPdGFBdnNrVklXMmZIV2E1djlyeXRmQmNFWVpZMmhSUGQ2RWwzS1hycnBMWVpBSG1LTDNVU0FodENwQWFnMC8zZTE4M1IvSUMrdUhnVFR3cmpob2Z5cFpKc1MzZ2IrMFQrWUhlK2ttUmk0RFdITnZocUhONW9wMWZrQ3JtQUZrSGszTWkrdWRiTXZIeVB1OUg5VExTNEJ2eU52b0IwRG1nMmhrMWpQcVg2NXFVYUlNQ3ZVNE40alZGWGhqc0V4TXhvYWhNWXN4Wk5CMjJGeTlYUUVHNDVxWUk0YW1lQjNzRWloRjIzNlJrZk5raHA2aUZlNUgwemkybjBqWnZEUkNVZ00wcGtOTkdTUzBvTWZLcU9DQWJBaUYrT1VtOGFNMk1BYzE0UVM2WnNic210ZGlLM2lHajhKL3hJWm53MmhXWWI4MENaRUF1Z2pHYklsVTZ5bXkyaFFKTjRrQWJrK3R2VnliNkt1UXRZMVU5aVJPUk1HNCtZeThaeGFCRWxDb0MwWm15cllrWUkrRVZIcVJUdHRtTTVDZjkxbkNZcU5zYkNMZnFVU29KTytTTTI2WFN2Mnp4ek9NRnFFQzBmZjltMGxKdEFuMmZJcXdWVTJTd1VINkNWVWlKT2w0bkR3S0l4VlEwSlZMSWc3Yi9WUXA5V2lISEYxL0FrSlI3VTNZMjZZZUkvQWtjVWpCZlMzUWYxTjFkVG1mcmVYMU9TcFpqYnM4ZXA2VzVyY3V3bGVreUFlR2h0QzlScW9VajNVaE96UGM0UVRtZlhYRHJpWG9KUnFhNEtVcTZOZEF4Z2hId0NpTFFWK3JpWFFrenhjUXQzUWtybTVyangzV1BtUHFpOXRBcWpZZWNadFlUVi9NTVJGblRYL21zNWpnNVk4UGdsVzl6bzE4Tm50TEovRXdXdFJnMjZ0WlJXNmlUZndEa3c9PSIsIm1hYyI6ImQ3OGZhYTc0NTQzZDcwZTcyNTMxMjM2YWJkOThlYTFkMGNlM2MzMGRmMGUyM2Y4YmQ4ZDkwNjViMTZmZGU3NGIiLCJ0YWciOiIifQ==',
'X-KT-Token':'602d6be0-f45b-474e-8674-0326effec7af',
'X-XSRF-TOKEN':'eyJpdiI6IkY2SGlIajhLUko2elM3MytmS2JDN2c9PSIsInZhbHVlIjoidEZkazBxWGJQUFZWaktpcFN2cHd2WG5ud1h0V1FOL3BMbHZIMHM3UGVCQWU5NXA1aTR6ZEJzZzMrRjcvZjRQaUxKL2RHT0s5QjRRUTNZRFB0Sy92SzRXb1M1bUd1SUZyY0pxRVQxMnExUEN4aWFtU1ZWZ0Rqb2dYSDQwUDVoOVYiLCJtYWMiOiI3NDY0NmE0NWJiZGFhNGYwNGJhZjIxODUwZWU5OGQzNDdlYTZjZGFjNDAxN2UxYTkxYjQwYzI2YzBlZGFjOTFhIiwidGFnIjoiIn0=',
'Content-Length':'166',
'Origin':'https://keywordtool.io',
'Connection':'keep-alive',
'Referer':'https://keywordtool.io',
# 'Cookie':'XSRF-TOKEN=eyJpdiI6IkY2SGlIajhLUko2elM3MytmS2JDN2c9PSIsInZhbHVlIjoidEZkazBxWGJQUFZWaktpcFN2cHd2WG5ud1h0V1FOL3BMbHZIMHM3UGVCQWU5NXA1aTR6ZEJzZzMrRjcvZjRQaUxKL2RHT0s5QjRRUTNZRFB0Sy92SzRXb1M1bUd1SUZyY0pxRVQxMnExUEN4aWFtU1ZWZ0Rqb2dYSDQwUDVoOVYiLCJtYWMiOiI3NDY0NmE0NWJiZGFhNGYwNGJhZjIxODUwZWU5OGQzNDdlYTZjZGFjNDAxN2UxYTkxYjQwYzI2YzBlZGFjOTFhIiwidGFnIjoiIn0%3D; keyword_tool_session=eyJpdiI6IkF3MktGQVlIWjJvSWdpS3R0YjJtcUE9PSIsInZhbHVlIjoiTmJ6cTI1Qys1SytQV0VqeWZQcWpoTkJ0TEFnNjQ0dlhTeG5oMlJBZUo4OEQrMDBRMml3cHFSN3JlWGZWSzk3Qmh5TTdQeWdNc2pFZkdoK1hKWWhjL2JBcUVzQVU1UHJ5QWYxZy9oUW9SQW9IQlQ3YkQ4azZweFNvUWd0a2lSMVMiLCJtYWMiOiIzMmVhMzc4ZDFmNmRhOTc5YTM3NGNjODljMWMwZjcxMGNkYTQyNDY5Zjk4ZDMyZThjODlmNWI2ZjQzZWRjYmNkIiwidGFnIjoiIn0%3D; current_locale=en; cf_zaraz_google-analytics_9587=true; google-analytics_9587___ga=dad8b701-78a2-40dd-94bf-f613baf2e8d4; _ga_3CKGCFMKLD=GS1.1.1686882181.1.1.1686887998.60.0.0; _ga=GA1.1.1668256117.1686882181; _clck=1dxjveq|2|fci|0|1262; google_search_engine=%7B%22category%22%3A%22web%22%2C%22country%22%3A%22GLB%22%2C%22language%22%3A%22en%22%2C%22location%22%3A%220%22%7D; google_locations_fav=%5B%220%7CGLB%7CGlobal%20%5C%2F%20Worldwide%20%28All%20Countries%29%22%5D; google_languages_fav=%5B%22en%7CEnglish%22%5D; keyword_search_count=6; cf_chl_2=dd02d2158528248; cf_clearance=lBeEaeBIFTX1b8kEUOttngFgfcjVH08YWXFDx4l5JOk-1686886775-0-160; last_search_engine=1; search_type_1=1; default_keyword_basket_search_engine=1; filters_settings=%7B%221%22%3A%7B%22filter_keywords%22%3A%5B%5D%7D%7D; negative_keywords=%5B%5D; last_sort_by_1=keywords; last_sort_direction_1=Desc; youtube_search_engine=%7B%22country%22%3A%22GLB%22%2C%22language%22%3A%22en%22%2C%22location%22%3A0%7D; youtube_locations_fav=%5B%220%7CGLB%7CGlobal%20%5C%2F%20Worldwide%20%28All%20Countries%29%22%5D; youtube_languages_fav=%5B%22en%7CEnglish%22%5D; search_type_2=1; __cf_bm=DfjBkyE1djdrKvwoey7bwX3M.GiDCnQIz6lpDxgKe94-1686886788-0-AfTJ+8VUM+mmK2418XGSXiHlLkm6dTp3Thr8e0xIpKvAQqWq+H5pCLYiuF5yS31R5A==; _clsk=13mvyzr|1686887966832|5|1|r.clarity.ms/collect',
'Sec-Fetch-Dest':'empty',
'Sec-Fetch-Mode':'cors',
'Sec-Fetch-Site':'same-origin',
'TE':'trailers ',
        }


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
                    
                    response = requests.get(f'https://keywordtool.io/search/keywords/google/result/67698?category=web&country=GLB&country_language=en&country_location=0&keyword={keywords}&language=en&metrics_country=GLB&metrics_currency=USD&metrics_is_default_location=0&metrics_is_estimated=0&metrics_language=1000&metrics_network=2&search_type=1&time=1686890218&signature=c8e404e1729665a8e89f758625a42a8c1c0637d7c42356327fb65badb5b3095a',  headers=headers, json= {},proxies={'http':None,'https':None}, timeout=timeout)
                    
                    headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
'Accept':'application/json, text/plain, */*',
'Accept-Language':'en-US,en;q=0.5',
'Accept-Encoding':'gzip, deflate, br',
'X-Requested-With':'XMLHttpRequest',
'Content-Type':'application/json',
'Token':'eyJpdiI6Ik94Y3doRjFmN2lHbmo2blhjVk9vekE9PSIsInZhbHVlIjoiUS93UGV2R05pRFdhczIxVEF0ZnhKZXlEVnNIc09MSXRnRUtkc2ZRaDVEeHFDamZkMnZNOE9hUHFIZ2lLM1RvOXJsZ08vY2toRWxHTWlKSXl5S0R3bldZM3E3Ykc5RVF3WFRxOEN5YTQwbUhvdGdjaTFjQU9seTRiVmlaV1c2SEI1L0NLbXJ3M2dOb1VrYm54ekgvMmNmUU9qTVdqYVNSTnVaY2FUVFc4Y1RmdFhKYXJGTHpnaExUaUM0ZkFKek5NVGo1dGJ5bjEyY3ZqM05SSnlyTjJNTHY2TUZtWjZ5SXFoYWpVMGc0UW5BZkgvOXNiQ1B0L3JURVQ2alQ0MTlGQkZpaGNsLzduRU54U2E4N1YybFZtYmJUSk5UWUxMMTNEM1VnVW8xQVEraGw1TmpJcGI4Y1hxQ3Y1WjRpQnJ3d0tLQzhXY3VETmVNQnFlSEVYMlpRd0ZQRUM4am5mL0dpV09xUnNDa0d2UFVpd0k2QklNWGp0MWhZYTl1a005bDA4YkhLQ3ZRcWV5eGJuQ0NHY21PcjF0VU9XN0xyRkcxY2tPckg0c1NvbVRRRGtUYmNPbW5jYkNSa0VKTDdSVGU4ZmdLMTB1c3lDMFNVODdoU0p5YWZDMmFrVFk4VHlNSzgvR1YyUTNldmVaTWV4LzgydFNnMFZyMG1OQjRnemU5TlVoNVhoWHhITGxKNHlXalRhV0xFLzNIVmQ0cE9vakZDSlhxT0dLVEMvYnRGa1cwZ0RwQXYvUEtYTW4wbmd6L1lpS3UzTXdGVVpTZzF0KzlaQnpPaHdZaWRVZm5pTDAzTVJzNEV4OUdtNmV4Y2JPSkZ5K1VRS1FBQ0kzd1FUa3hTT1VCTmJsOGtmajl1NUQ4OVZ0WWRXdGNMbXI4UG1NaFhtcG9ucE55T1RubGRBWFp0RS9QbFppTG5PVHljYzdJcUR6YUpFVE5EdlhaalYwZW4wTzYxUXNPdGFBdnNrVklXMmZIV2E1djlyeXRmQmNFWVpZMmhSUGQ2RWwzS1hycnBMWVpBSG1LTDNVU0FodENwQWFnMC8zZTE4M1IvSUMrdUhnVFR3cmpob2Z5cFpKc1MzZ2IrMFQrWUhlK2ttUmk0RFdITnZocUhONW9wMWZrQ3JtQUZrSGszTWkrdWRiTXZIeVB1OUg5VExTNEJ2eU52b0IwRG1nMmhrMWpQcVg2NXFVYUlNQ3ZVNE40alZGWGhqc0V4TXhvYWhNWXN4Wk5CMjJGeTlYUUVHNDVxWUk0YW1lQjNzRWloRjIzNlJrZk5raHA2aUZlNUgwemkybjBqWnZEUkNVZ00wcGtOTkdTUzBvTWZLcU9DQWJBaUYrT1VtOGFNMk1BYzE0UVM2WnNic210ZGlLM2lHajhKL3hJWm53MmhXWWI4MENaRUF1Z2pHYklsVTZ5bXkyaFFKTjRrQWJrK3R2VnliNkt1UXRZMVU5aVJPUk1HNCtZeThaeGFCRWxDb0MwWm15cllrWUkrRVZIcVJUdHRtTTVDZjkxbkNZcU5zYkNMZnFVU29KTytTTTI2WFN2Mnp4ek9NRnFFQzBmZjltMGxKdEFuMmZJcXdWVTJTd1VINkNWVWlKT2w0bkR3S0l4VlEwSlZMSWc3Yi9WUXA5V2lISEYxL0FrSlI3VTNZMjZZZUkvQWtjVWpCZlMzUWYxTjFkVG1mcmVYMU9TcFpqYnM4ZXA2VzVyY3V3bGVreUFlR2h0QzlScW9VajNVaE96UGM0UVRtZlhYRHJpWG9KUnFhNEtVcTZOZEF4Z2hId0NpTFFWK3JpWFFrenhjUXQzUWtybTVyangzV1BtUHFpOXRBcWpZZWNadFlUVi9NTVJGblRYL21zNWpnNVk4UGdsVzl6bzE4Tm50TEovRXdXdFJnMjZ0WlJXNmlUZndEa3c9PSIsIm1hYyI6ImQ3OGZhYTc0NTQzZDcwZTcyNTMxMjM2YWJkOThlYTFkMGNlM2MzMGRmMGUyM2Y4YmQ4ZDkwNjViMTZmZGU3NGIiLCJ0YWciOiIifQ==',
'X-KT-Token':'602d6be0-f45b-474e-8674-0326effec7af',
'X-XSRF-TOKEN':'eyJpdiI6IkY2SGlIajhLUko2elM3MytmS2JDN2c9PSIsInZhbHVlIjoidEZkazBxWGJQUFZWaktpcFN2cHd2WG5ud1h0V1FOL3BMbHZIMHM3UGVCQWU5NXA1aTR6ZEJzZzMrRjcvZjRQaUxKL2RHT0s5QjRRUTNZRFB0Sy92SzRXb1M1bUd1SUZyY0pxRVQxMnExUEN4aWFtU1ZWZ0Rqb2dYSDQwUDVoOVYiLCJtYWMiOiI3NDY0NmE0NWJiZGFhNGYwNGJhZjIxODUwZWU5OGQzNDdlYTZjZGFjNDAxN2UxYTkxYjQwYzI2YzBlZGFjOTFhIiwidGFnIjoiIn0=',
'Content-Length':'166',
'Origin':'https://keywordtool.io',
'Connection':'keep-alive',
'Referer':f'https://keywordtool.io/search/keywords/google/result/67698?category=web&country=GLB&country_language=en&country_location=0&keyword={keywords}&language=en&metrics_country=GLB&metrics_currency=USD&metrics_is_default_location=0&metrics_is_estimated=0&metrics_language=1000&metrics_network=2&search_type=1&time=1686890218&signature=c8e404e1729665a8e89f758625a42a8c1c0637d7c42356327fb65badb5b3095a',
# 'Cookie':'XSRF-TOKEN=eyJpdiI6IkY2SGlIajhLUko2elM3MytmS2JDN2c9PSIsInZhbHVlIjoidEZkazBxWGJQUFZWaktpcFN2cHd2WG5ud1h0V1FOL3BMbHZIMHM3UGVCQWU5NXA1aTR6ZEJzZzMrRjcvZjRQaUxKL2RHT0s5QjRRUTNZRFB0Sy92SzRXb1M1bUd1SUZyY0pxRVQxMnExUEN4aWFtU1ZWZ0Rqb2dYSDQwUDVoOVYiLCJtYWMiOiI3NDY0NmE0NWJiZGFhNGYwNGJhZjIxODUwZWU5OGQzNDdlYTZjZGFjNDAxN2UxYTkxYjQwYzI2YzBlZGFjOTFhIiwidGFnIjoiIn0%3D; keyword_tool_session=eyJpdiI6IkF3MktGQVlIWjJvSWdpS3R0YjJtcUE9PSIsInZhbHVlIjoiTmJ6cTI1Qys1SytQV0VqeWZQcWpoTkJ0TEFnNjQ0dlhTeG5oMlJBZUo4OEQrMDBRMml3cHFSN3JlWGZWSzk3Qmh5TTdQeWdNc2pFZkdoK1hKWWhjL2JBcUVzQVU1UHJ5QWYxZy9oUW9SQW9IQlQ3YkQ4azZweFNvUWd0a2lSMVMiLCJtYWMiOiIzMmVhMzc4ZDFmNmRhOTc5YTM3NGNjODljMWMwZjcxMGNkYTQyNDY5Zjk4ZDMyZThjODlmNWI2ZjQzZWRjYmNkIiwidGFnIjoiIn0%3D; current_locale=en; cf_zaraz_google-analytics_9587=true; google-analytics_9587___ga=dad8b701-78a2-40dd-94bf-f613baf2e8d4; _ga_3CKGCFMKLD=GS1.1.1686882181.1.1.1686887998.60.0.0; _ga=GA1.1.1668256117.1686882181; _clck=1dxjveq|2|fci|0|1262; google_search_engine=%7B%22category%22%3A%22web%22%2C%22country%22%3A%22GLB%22%2C%22language%22%3A%22en%22%2C%22location%22%3A%220%22%7D; google_locations_fav=%5B%220%7CGLB%7CGlobal%20%5C%2F%20Worldwide%20%28All%20Countries%29%22%5D; google_languages_fav=%5B%22en%7CEnglish%22%5D; keyword_search_count=6; cf_chl_2=dd02d2158528248; cf_clearance=lBeEaeBIFTX1b8kEUOttngFgfcjVH08YWXFDx4l5JOk-1686886775-0-160; last_search_engine=1; search_type_1=1; default_keyword_basket_search_engine=1; filters_settings=%7B%221%22%3A%7B%22filter_keywords%22%3A%5B%5D%7D%7D; negative_keywords=%5B%5D; last_sort_by_1=keywords; last_sort_direction_1=Desc; youtube_search_engine=%7B%22country%22%3A%22GLB%22%2C%22language%22%3A%22en%22%2C%22location%22%3A0%7D; youtube_locations_fav=%5B%220%7CGLB%7CGlobal%20%5C%2F%20Worldwide%20%28All%20Countries%29%22%5D; youtube_languages_fav=%5B%22en%7CEnglish%22%5D; search_type_2=1; __cf_bm=DfjBkyE1djdrKvwoey7bwX3M.GiDCnQIz6lpDxgKe94-1686886788-0-AfTJ+8VUM+mmK2418XGSXiHlLkm6dTp3Thr8e0xIpKvAQqWq+H5pCLYiuF5yS31R5A==; _clsk=13mvyzr|1686887966832|5|1|r.clarity.ms/collect',
'Sec-Fetch-Dest':'empty',
'Sec-Fetch-Mode':'cors',
'Sec-Fetch-Site':'same-origin',
'TE':'trailers ',
        }
                    
                    response = requests.post(f'https://keywordtool.io/search/keywords/google/keywords',  headers=headers, json= {},proxies={'http':None,'https':None}, timeout=timeout)

                    
                    print('====\r',response.content())
                    if 'keywords_payload' in response.json():
                        keywords_payload=response.json()['keywords_payload']
                    metricURL=response.json()['metrics_url']
                    if '?signature=' in metricURL:
                        signature=metricURL.split('?signature=')[-1]
                    scrape_urls=response.json()['scrape_urls']
                    if keywords_payload:
                        response = requests.post(metricURL,  headers=headers, json= json_data,proxies={'http':None,'https':None}, timeout=timeout)
                    
                    json_data = {"filter_keywords":"","filter_keywords_partial_match":"","negative_keywords":"","keywords_payload":keywords_payload,"sort":"keywordsAsc","total":100}
                    data=json.dumps(json_data)
                    response.raise_for_status()
                    
                    response = requests.post(metricURL,  headers=headers, json= json_data,proxies={'http':None,'https':None}, timeout=timeout)

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
