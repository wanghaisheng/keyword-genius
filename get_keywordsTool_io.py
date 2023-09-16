import requests
import base64
import os
import time
from traceback import print_exc
import random
import json
from time import sleep
from requests.exceptions import Timeout
import shutil
import zipfile

def zip_folder(folder_path, output_folder, max_size_mb, zip_file,zip_temp_file,zip_count):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Convert the maximum size from MB to bytes
    max_size_bytes = max_size_mb * 1024 * 1024

    # Iterate over the directory tree
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            # Add each file to the current ZIP archive
            zip_file.write(file_path)

            # Check if the current ZIP file exceeds the maximum size
            if os.stat(file_path).st_size > max_size_bytes:
                # Close the current ZIP archive
                zip_file.close()

                # Move the current ZIP file to the output folder
                shutil.move(
                    zip_temp_file,
                    os.path.join(output_folder, f"archive{zip_count}.zip"),
                )

                print(
                    f"Created 'archive{zip_count}.zip' (size: {os.path.getsize(os.path.join(output_folder, f'archive{zip_count}.zip'))} bytes)"
                )

                # Create a new ZIP archive for the remaining files
                zip_count += 1
                zip_temp_file = os.path.join(output_folder, f"temp{zip_count}.zip")
                zip_file = zipfile.ZipFile(zip_temp_file, "w", zipfile.ZIP_DEFLATED)

                # Delete the original file after adding it to the ZIP archive
                os.remove(file_path)

    # Close the last ZIP archive
    zip_file.close()

    # Move the last ZIP file to the output folder
    shutil.move(zip_temp_file, os.path.join(output_folder, f"archive{zip_count}.zip"))

    print(
        f"Created 'archive{zip_count}.zip' (size: {os.path.getsize(os.path.join(output_folder, f'archive{zip_count}.zip'))} bytes)"
    )


def get(keywords):
    try:
        headers = {
            "Host": "keywordtool.io",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": "https://keywordtool.io/",
            "Cookie": "XSRF-TOKEN=eyJpdiI6InBXMFN2TFgzVkpPWis3NU5xMWRVUnc9PSIsInZhbHVlIjoiYkVsVG9KZFQ4a1lkdnkxeTZzRGNKZkU3eWcvN2laUzl1aGZkdmFtZlNYNlY2a0xYZFRDbmlQbGVTZFZRU2xLV1JmREoxT2drK2c0KzgrY1Y5Z1EvYjlaSXl4SmQ0cjNhMkxwNmo1N1Z1RzA4UkVpT0xzTFdNMzhzTHVMaEFiMEUiLCJtYWMiOiI0ZWMwZGRiMzhjMjAzYjliNTRjYzhkYjlmZTc3MjdhMjc1ZTI3N2Y1MDdlZmY4ZDgwOWNkOGJhZDgxZWNkYmYxIiwidGFnIjoiIn0%3D; keyword_tool_session=eyJpdiI6Ik5aa0YzZFZ4SW1GOGJISzdOcTBGNFE9PSIsInZhbHVlIjoiL3ZwU29LUUZxSTdUK09RR3BQUjA4WXhBV0dhTHZIUlZGUnh2QWhWNVVuMThZOG9xSmo4MmJXb2VMYzNhcC93NWwweStyU2RxQjR5NElKUTF0d0dpM1JYQVkyWnhsaGhSd04xT0RGM0NZV1l1YXZaTXFqR2t1RmFjcjR3L2dwZWYiLCJtYWMiOiJjNTBkMjRjY2Q1MTBhMTNjMTEwNWY2NDE4NDM3MzhiNWViY2JkNGFjNWY5ZTMxYTdhMjRkOWU0MzUwNDQxZWUxIiwidGFnIjoiIn0%3D; current_locale=en; cf_zaraz_google-analytics_9587=true; google-analytics_9587___ga=dad8b701-78a2-40dd-94bf-f613baf2e8d4; _ga_3CKGCFMKLD=GS1.1.1686882181.1.1.1686890217.33.0.0; _ga=GA1.1.1668256117.1686882181; _clck=1dxjveq|2|fci|0|1262; google_search_engine=%7B%22category%22%3A%22web%22%2C%22country%22%3A%22GLB%22%2C%22language%22%3A%22en%22%2C%22location%22%3A%220%22%7D; google_locations_fav=%5B%220%7CGLB%7CGlobal%20%5C%2F%20Worldwide%20%28All%20Countries%29%22%5D; google_languages_fav=%5B%22en%7CEnglish%22%5D; keyword_search_count=9; cf_chl_2=27c7fc2ee7445c3; cf_clearance=DKHGUEgxhZiSeKlmlr_iWjfifNbUvy0PuDtBqvT7e.w-1686889104-0-160; last_search_engine=1; search_type_1=1; default_keyword_basket_search_engine=1; filters_settings=%7B%221%22%3A%7B%22filter_keywords%22%3A%5B%5D%7D%7D; negative_keywords=%5B%5D; last_sort_by_1=keywords; last_sort_direction_1=Desc; youtube_search_engine=%7B%22country%22%3A%22GLB%22%2C%22language%22%3A%22en%22%2C%22location%22%3A0%7D; youtube_locations_fav=%5B%220%7CGLB%7CGlobal%20%5C%2F%20Worldwide%20%28All%20Countries%29%22%5D; youtube_languages_fav=%5B%22en%7CEnglish%22%5D; search_type_2=1; _clsk=13mvyzr|1686890202369|14|1|r.clarity.ms/collect; __cf_bm=h9voHucrS3H7QTIwYUiGCXWM5qjMFj_Ay3NsMPlXvGw-1686888867-0-AemZ3OCeNXVlxxxMggDBk+g88e/MgBJoBpHooE3lXi/6Y85rjWPLQoXeg1kzfZj2pQ==",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "TE": "trailers",
        }

        # json serializes Python dictionaries to JSON. data takes arbitrary bytes.

        max_retries = 3
        timeout = 15
        platforms = [
            "google",
            "youtube",
            "bing",
            "amazon",
            "ebay",
            "app-store",
            "play-store",
            "instagram",
            "twitter",
            "pinterest",
            "google-trends",
        ]
        # to-do  tiktok douyin xiaohongshu tiktok ads  facebook ads
        search_types = [1, 3, 6]
        #  Keyword Suggestions 1
        # Questions 3
        # Prepositions 6
        for platform in platforms:
            print("start to deal keyword:", keywords)

            print("start to deal platform:", platform)
            for search_type in search_types:
                print(
                    "start to deal with type:Keyword Suggestions 1,Questions 3,Prepositions 6=====:",
                    str(search_type),
                )

                fname = keywords.strip()
                fname = fname + "-" + platform + "-" + str(search_type)
                if not os.path.exists("./output/" + fname + ".json"):
                    print("file is not yet :", "./output/" + fname + ".json")
                    url= f"https://keywordtool.io/search/keywords/{platform}/result/67698?category=web&country=GLB&country_language=en&country_location=0&keyword={keywords}&language=en&metrics_country=GLB&metrics_currency=USD&metrics_is_default_location=0&metrics_is_estimated=0&metrics_language=1000&metrics_network=2&search_type=1&time=1686890218&signature=c8e404e1729665a8e89f758625a42a8c1c0637d7c42356327fb65badb5b3095a"
                    retry_count = 0
                    while retry_count < max_retries:
                        try:
                            response = requests.get(
                               url,
                                headers=headers,
                                json={},
                                proxies={"http": None, "https": None},
                                timeout=timeout,
                            )
                            print(f"first get response:{url}", response.status_code)
                            headers = {
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0",
                                "Accept": "application/json, text/plain, */*",
                                "Accept-Language": "en-US,en;q=0.5",
                                "Accept-Encoding": "gzip, deflate, br",
                                "X-Requested-With": "XMLHttpRequest",
                                "Content-Type": "application/json",
                                "Token": "eyJpdiI6Ik94Y3doRjFmN2lHbmo2blhjVk9vekE9PSIsInZhbHVlIjoiUS93UGV2R05pRFdhczIxVEF0ZnhKZXlEVnNIc09MSXRnRUtkc2ZRaDVEeHFDamZkMnZNOE9hUHFIZ2lLM1RvOXJsZ08vY2toRWxHTWlKSXl5S0R3bldZM3E3Ykc5RVF3WFRxOEN5YTQwbUhvdGdjaTFjQU9seTRiVmlaV1c2SEI1L0NLbXJ3M2dOb1VrYm54ekgvMmNmUU9qTVdqYVNSTnVaY2FUVFc4Y1RmdFhKYXJGTHpnaExUaUM0ZkFKek5NVGo1dGJ5bjEyY3ZqM05SSnlyTjJNTHY2TUZtWjZ5SXFoYWpVMGc0UW5BZkgvOXNiQ1B0L3JURVQ2alQ0MTlGQkZpaGNsLzduRU54U2E4N1YybFZtYmJUSk5UWUxMMTNEM1VnVW8xQVEraGw1TmpJcGI4Y1hxQ3Y1WjRpQnJ3d0tLQzhXY3VETmVNQnFlSEVYMlpRd0ZQRUM4am5mL0dpV09xUnNDa0d2UFVpd0k2QklNWGp0MWhZYTl1a005bDA4YkhLQ3ZRcWV5eGJuQ0NHY21PcjF0VU9XN0xyRkcxY2tPckg0c1NvbVRRRGtUYmNPbW5jYkNSa0VKTDdSVGU4ZmdLMTB1c3lDMFNVODdoU0p5YWZDMmFrVFk4VHlNSzgvR1YyUTNldmVaTWV4LzgydFNnMFZyMG1OQjRnemU5TlVoNVhoWHhITGxKNHlXalRhV0xFLzNIVmQ0cE9vakZDSlhxT0dLVEMvYnRGa1cwZ0RwQXYvUEtYTW4wbmd6L1lpS3UzTXdGVVpTZzF0KzlaQnpPaHdZaWRVZm5pTDAzTVJzNEV4OUdtNmV4Y2JPSkZ5K1VRS1FBQ0kzd1FUa3hTT1VCTmJsOGtmajl1NUQ4OVZ0WWRXdGNMbXI4UG1NaFhtcG9ucE55T1RubGRBWFp0RS9QbFppTG5PVHljYzdJcUR6YUpFVE5EdlhaalYwZW4wTzYxUXNPdGFBdnNrVklXMmZIV2E1djlyeXRmQmNFWVpZMmhSUGQ2RWwzS1hycnBMWVpBSG1LTDNVU0FodENwQWFnMC8zZTE4M1IvSUMrdUhnVFR3cmpob2Z5cFpKc1MzZ2IrMFQrWUhlK2ttUmk0RFdITnZocUhONW9wMWZrQ3JtQUZrSGszTWkrdWRiTXZIeVB1OUg5VExTNEJ2eU52b0IwRG1nMmhrMWpQcVg2NXFVYUlNQ3ZVNE40alZGWGhqc0V4TXhvYWhNWXN4Wk5CMjJGeTlYUUVHNDVxWUk0YW1lQjNzRWloRjIzNlJrZk5raHA2aUZlNUgwemkybjBqWnZEUkNVZ00wcGtOTkdTUzBvTWZLcU9DQWJBaUYrT1VtOGFNMk1BYzE0UVM2WnNic210ZGlLM2lHajhKL3hJWm53MmhXWWI4MENaRUF1Z2pHYklsVTZ5bXkyaFFKTjRrQWJrK3R2VnliNkt1UXRZMVU5aVJPUk1HNCtZeThaeGFCRWxDb0MwWm15cllrWUkrRVZIcVJUdHRtTTVDZjkxbkNZcU5zYkNMZnFVU29KTytTTTI2WFN2Mnp4ek9NRnFFQzBmZjltMGxKdEFuMmZJcXdWVTJTd1VINkNWVWlKT2w0bkR3S0l4VlEwSlZMSWc3Yi9WUXA5V2lISEYxL0FrSlI3VTNZMjZZZUkvQWtjVWpCZlMzUWYxTjFkVG1mcmVYMU9TcFpqYnM4ZXA2VzVyY3V3bGVreUFlR2h0QzlScW9VajNVaE96UGM0UVRtZlhYRHJpWG9KUnFhNEtVcTZOZEF4Z2hId0NpTFFWK3JpWFFrenhjUXQzUWtybTVyangzV1BtUHFpOXRBcWpZZWNadFlUVi9NTVJGblRYL21zNWpnNVk4UGdsVzl6bzE4Tm50TEovRXdXdFJnMjZ0WlJXNmlUZndEa3c9PSIsIm1hYyI6ImQ3OGZhYTc0NTQzZDcwZTcyNTMxMjM2YWJkOThlYTFkMGNlM2MzMGRmMGUyM2Y4YmQ4ZDkwNjViMTZmZGU3NGIiLCJ0YWciOiIifQ==",
                                "X-KT-Token": "602d6be0-f45b-474e-8674-0326effec7af",
                                "X-XSRF-TOKEN": "eyJpdiI6IkY2SGlIajhLUko2elM3MytmS2JDN2c9PSIsInZhbHVlIjoidEZkazBxWGJQUFZWaktpcFN2cHd2WG5ud1h0V1FOL3BMbHZIMHM3UGVCQWU5NXA1aTR6ZEJzZzMrRjcvZjRQaUxKL2RHT0s5QjRRUTNZRFB0Sy92SzRXb1M1bUd1SUZyY0pxRVQxMnExUEN4aWFtU1ZWZ0Rqb2dYSDQwUDVoOVYiLCJtYWMiOiI3NDY0NmE0NWJiZGFhNGYwNGJhZjIxODUwZWU5OGQzNDdlYTZjZGFjNDAxN2UxYTkxYjQwYzI2YzBlZGFjOTFhIiwidGFnIjoiIn0=",
                                "Content-Length": "166",
                                "Origin": "https://keywordtool.io",
                                "Connection": "keep-alive",
                                "Referer": f"https://keywordtool.io/search/keywords/{platform}/result/67698?category=web&country=GLB&country_language=en&country_location=0&keyword={keywords}&language=en&metrics_country=GLB&metrics_currency=USD&metrics_is_default_location=0&metrics_is_estimated=0&metrics_language=1000&metrics_network=2&search_type={search_type}&time=1686890218&signature=c8e404e1729665a8e89f758625a42a8c1c0637d7c42356327fb65badb5b3095a",
                                # 'Cookie':'XSRF-TOKEN=eyJpdiI6IkY2SGlIajhLUko2elM3MytmS2JDN2c9PSIsInZhbHVlIjoidEZkazBxWGJQUFZWaktpcFN2cHd2WG5ud1h0V1FOL3BMbHZIMHM3UGVCQWU5NXA1aTR6ZEJzZzMrRjcvZjRQaUxKL2RHT0s5QjRRUTNZRFB0Sy92SzRXb1M1bUd1SUZyY0pxRVQxMnExUEN4aWFtU1ZWZ0Rqb2dYSDQwUDVoOVYiLCJtYWMiOiI3NDY0NmE0NWJiZGFhNGYwNGJhZjIxODUwZWU5OGQzNDdlYTZjZGFjNDAxN2UxYTkxYjQwYzI2YzBlZGFjOTFhIiwidGFnIjoiIn0%3D; keyword_tool_session=eyJpdiI6IkF3MktGQVlIWjJvSWdpS3R0YjJtcUE9PSIsInZhbHVlIjoiTmJ6cTI1Qys1SytQV0VqeWZQcWpoTkJ0TEFnNjQ0dlhTeG5oMlJBZUo4OEQrMDBRMml3cHFSN3JlWGZWSzk3Qmh5TTdQeWdNc2pFZkdoK1hKWWhjL2JBcUVzQVU1UHJ5QWYxZy9oUW9SQW9IQlQ3YkQ4azZweFNvUWd0a2lSMVMiLCJtYWMiOiIzMmVhMzc4ZDFmNmRhOTc5YTM3NGNjODljMWMwZjcxMGNkYTQyNDY5Zjk4ZDMyZThjODlmNWI2ZjQzZWRjYmNkIiwidGFnIjoiIn0%3D; current_locale=en; cf_zaraz_google-analytics_9587=true; google-analytics_9587___ga=dad8b701-78a2-40dd-94bf-f613baf2e8d4; _ga_3CKGCFMKLD=GS1.1.1686882181.1.1.1686887998.60.0.0; _ga=GA1.1.1668256117.1686882181; _clck=1dxjveq|2|fci|0|1262; google_search_engine=%7B%22category%22%3A%22web%22%2C%22country%22%3A%22GLB%22%2C%22language%22%3A%22en%22%2C%22location%22%3A%220%22%7D; google_locations_fav=%5B%220%7CGLB%7CGlobal%20%5C%2F%20Worldwide%20%28All%20Countries%29%22%5D; google_languages_fav=%5B%22en%7CEnglish%22%5D; keyword_search_count=6; cf_chl_2=dd02d2158528248; cf_clearance=lBeEaeBIFTX1b8kEUOttngFgfcjVH08YWXFDx4l5JOk-1686886775-0-160; last_search_engine=1; search_type_1=1; default_keyword_basket_search_engine=1; filters_settings=%7B%221%22%3A%7B%22filter_keywords%22%3A%5B%5D%7D%7D; negative_keywords=%5B%5D; last_sort_by_1=keywords; last_sort_direction_1=Desc; youtube_search_engine=%7B%22country%22%3A%22GLB%22%2C%22language%22%3A%22en%22%2C%22location%22%3A0%7D; youtube_locations_fav=%5B%220%7CGLB%7CGlobal%20%5C%2F%20Worldwide%20%28All%20Countries%29%22%5D; youtube_languages_fav=%5B%22en%7CEnglish%22%5D; search_type_2=1; __cf_bm=DfjBkyE1djdrKvwoey7bwX3M.GiDCnQIz6lpDxgKe94-1686886788-0-AfTJ+8VUM+mmK2418XGSXiHlLkm6dTp3Thr8e0xIpKvAQqWq+H5pCLYiuF5yS31R5A==; _clsk=13mvyzr|1686887966832|5|1|r.clarity.ms/collect',
                                "Sec-Fetch-Dest": "empty",
                                "Sec-Fetch-Mode": "cors",
                                "Sec-Fetch-Site": "same-origin",
                                "TE": "trailers ",
                            }

                            response = requests.post(
                                f"https://keywordtool.io/search/keywords/{platform}/keywords",
                                headers=headers,
                                json={},
                                proxies={"http": None, "https": None},
                                timeout=timeout,
                            )
                            print(f"{platform}-{search_type}-post response", response)

                            # print('====\r',response.json())
                            if "keywords_payload" in response.json():
                                keywords_payload = response.json()["keywords_payload"]
                                print("====keywords_payload\r", keywords_payload)
                                
                                data = json.dumps(json_data)
                                response.raise_for_status()
                                if keywords_payload:
                                    sleep_time = random.uniform(1, 3)
                                    print(f"Sleeping for {sleep_time} seconds...")
                                    time.sleep(sleep_time)

                                    response = requests.post(
                                        metricURL,
                                        headers=headers,
                                        json=json_data,
                                        proxies={"http": None, "https": None},
                                        timeout=timeout,
                                    )
                                    print("3 post response", response.status_code)

                                    print(f"{platform}-{search_type}-Request successful!")
                                    try:
                                        result = response.json()["all_keywords"]
                                        # print('====all_keywords\r',result)

                                        if not os.path.exists("./output"):
                                            os.mkdir("./output")
                                            print("create result folder")

                                        with open(
                                            "./output/" + fname + ".json",
                                            "w",
                                            encoding="utf-8",
                                        ) as f:
                                            print(f"write {search_type}result json ")

                                            json.dump(
                                                result, f, ensure_ascii=False, indent=4
                                            )

                                        with open(
                                            "./output/" + fname + "-scrape_urls.json",
                                            "w",
                                            encoding="utf-8",
                                        ) as f:
                                            print(f"write {search_type} scrape_urls json ")

                                            json.dump(
                                                scrape_urls, f, ensure_ascii=False, indent=4
                                            )
                                        break
                                    except:
                                        print(
                                            "response content has no audio data filed",
                                            response.status_code,
                                        )
                                        retry_count += 1
                                
                            else:
                                print("====keywords_payload not found")

                            if "metrics_url" in response.json():
                                metricURL = response.json()["metrics_url"]
                                print("====metricURL\r", metricURL)

                                if "?signature=" in metricURL:
                                    signature = metricURL.split("?signature=")[-1]
                                    print("====signature\r", signature)
                            else:
                                print("====metrics_url not found")                                    
                            if "scrape_urls" in response.json():
                                scrape_urls = response.json()["scrape_urls"]
                            else:
                                print("====scrape_urls not found")
                            json_data = {
                                "filter_keywords": "",
                                "filter_keywords_partial_match": "",
                                "negative_keywords": "",
                                "keywords_payload": keywords_payload,
                                "sort": "keywordsAsc",
                                "total": 100,
                            }

                        except Timeout:
                            print("Request timed out. Retrying...")
                            retry_count += 1
                        except requests.RequestException as e:
                            print("An error occurred:", e)
                    if retry_count == max_retries:
                        print("Maximum number of retries reached.")
                    print("this one is done")

    except:
        print_exc()
        return None

output_folder = "./output"
folder_path =  "./output"

if not os.path.exists("output"):
    os.mkdir("output")
    
keywords = os.getenv("Keywords")
# keywords = "capcut", "temu"

if keywords:
    if "," in keywords:
        keywords = list(keywords)
    else:
        keywords = [keywords]
    print('inputs:\r',keywords)
    for k in keywords:
        get(k)

max_size_mb = 1500

# Create a temporary ZIP file for the first archive
zip_count = 1
zip_temp_file = os.path.join(output_folder, f"temp{zip_count}.zip")
zip_file = zipfile.ZipFile(zip_temp_file, "w", zipfile.ZIP_DEFLATED)

    # Compress the folder into multiple ZIP archives
zip_folder(folder_path, output_folder, max_size_mb, zip_file,zip_temp_file,zip_count)
