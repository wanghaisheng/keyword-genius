# https://sale.1688.com/factory/home.html?spm=a260k.22518165.kzntrlke.2.323e5c68LsjqeU
# 从品类进去
# 还有热度榜
# https://sale.1688.com/factory/bd_new.html?spm=a260k.22464671.home2019category.57.6ce97a6eIEHQ2R&id=1753

# https://sale.1688.com/factory/bd_new.html?spm=a260k.24006001.l0aos5ys.47.3f014d84CdrXNs&id=201561112

# https://mind.1688.com/industry/common-Industry/2H7JMafwk4/index.html?spm=a260k.22518165.mainDoor.4.1ecc5c68F4fMXw&wh_pha=true&wh_pid=2702060&__pageId__=2702060&__existtitle__=1&__removesafearea__=true&_wvUseWKWebView=true

# https://sale.1688.com/factory/bd_new_category.html?spm=a260k.19776607.kyttffd8.4.40df4d84hQBu4C

# https://sale.1688.com/factory/bd_power_category.html?spm=a260k.19776607.kyttffd8.1.40df4d84hQBu4C

# https://sale.1688.com/factory/bd_hot_category.html?spm=a260k.19776607.kyttffd8.2.40df4d84hQBu4C

# https://sale.1688.com/factory/bd_power_category.html?spm=a260k.19776607.kyttffd8.1.40df4d84hQBu4C
# https://sale.1688.com/factory/bd_serve.html?id=1043174

import sys
import time
import random
import tkinter
from threading import Thread
import logging
import os
import pandas as pd
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed

from DrissionPage import (
    ChromiumOptions,
    ChromiumPage,
    SessionPage,
    WebPage,
    SessionOptions,
)

from DataRecorder import Recorder, DBRecorder
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Style

init()

# Define the semaphore with a limit, for example, 3 concurrent tasks
concurrent_limit = 10
semaphore = asyncio.Semaphore(concurrent_limit)


# Update the test_proxy function
def test_proxy(proxy_url):
    test_url = "https://sale.1688.com"

    try:
        print(f"test {[proxy_url]}")
        response = requests.get(
            test_url,
            proxies={"http": proxy_url, "https": proxy_url},
            timeout=10,
            # , verify=False
        )
        print(f"{Style.BRIGHT}{Fore.GREEN}Valid Proxy | {proxy_url}{Style.RESET_ALL}")
        if response.status_code != 200:
            valid_proxies.remove(proxy_url)
            print(
                f"{Style.BRIGHT}{Fore.RED}Invalid Proxy | {proxy_url}{Style.RESET_ALL}"
            )

        #     soup = BeautifulSoup(response.content, "lxml")
        #     if "captcha" in str(soup):
    except requests.exceptions.RequestException:

        valid_proxies.remove(proxy_url)
        print(f"{Style.BRIGHT}{Fore.RED}Invalid Proxy | {proxy_url}{Style.RESET_ALL}")


def get_proxy():
    return requests.get("http://demo.spiderpy.cn/get").json()


async def getbangdandetail(key, title, cat_1, cat_2, url, valid_proxies, semaphore):
    async with semaphore:  # Acquire the semaphore before starting the task

        max_retries = 3
        for i in range(max_retries):
            valid_proxies = [p for p in valid_proxies if p is not None]
            pro_str = random.choice(valid_proxies)
            proxy = "http://{}".format(pro_str)

            # proxy = f"http://{rand_proxies()}"
            print(f"try {proxy}")
            proxies = {"http": proxy, "https": proxy.replace("http", "https")}

            # co = ChromiumOptions().auto_port()
            # pro_str = get_proxy()["proxy"]

            # proxy = "http://{}".format(pro_str)
            # co.set_proxy(proxy.replace("http", "https"))
            # co.set_proxy(proxy)

            # page = ChromiumPage(co)

            so = SessionOptions()
            so.set_proxies(proxies)
            page = SessionPage(so)
            try:
                page.get(url)

                tab = page
                faclist = tab.ele("#rank-list").children()
                #     print(faclist)
                print(f"found {len(faclist)} for cat {cat_1} -{cat_2}-{key} ")
                # print(f"detect click more:")

                # count = 1
                # while True:

                #     try:
                #         tab.ele("text=查看更多")

                #         print(f"找到了{count}查看更多")
                #         tab.ele("text=查看更多").click()
                #         count = count + 1
                #         tab.run_js("document.documentElement.scrollTop=1000")
                #         # time.sleep(5)s
                #     except:
                #         print("没有找到。")
                #         break
                #     print(page.html)
                #  session mode 无法点击 但chromnium 模式下代理又不起作用
                # time.sleep(3)
                # faclist = tab.eles("@data-tracker=zgc-factory-item")
                faclist = tab.ele("#rank-list").children()
                #     print(faclist)
                print(f"found {len(faclist)} for cat {cat_1} -{cat_2}-{key} ")
                for i in range(0, len(faclist)):
                    print(f"do {i}")

                    try:

                        # print(type(e))
                        e = faclist[i].ele("tag:a")
                        print(
                            f"========={i}-for cat {cat_1} -{cat_2}-{key}============"
                        )
                        # link = e.ele("tag:a").link
                        link = e.link
                        text = e.texts()
                        #     text = e.text
                        data = {
                            "key": key,
                            "title": title,
                            "cat1": cat_1,
                            "cat2": cat_2,
                            "type": "ranklist",
                            "url": url,
                            "link": link,
                            "factory_info": text,
                            "json": "",
                        }
                        print(f"add {i} data for cat {cat_1} -{cat_2}-{key} \r {data}")
                        factoryinranklinkfile.add_data(data)
                        factoryinranklinkdb.add_data(data)
                        # page.close()
                        # return data
                    except:
                        # print(faclist[i].inner_html)

                        print(f"{i} we cannot find  data")

                if tab.ele("#recommend-list"):
                    faclist = tab.ele("#recommend-list").eles(".factory-item")

                    print(
                        f"found {len(faclist)}  recommend for cat {cat_1} -{cat_2}-{key} "
                    )
                    for i in range(0, len(faclist)):
                        print(f"do recommend {i}")

                        # print(type(e))

                        try:
                            e = faclist[i]
                            print(
                                f"========={i}-for cat {cat_1} -{cat_2}-{key}============"
                            )
                            json = e.attr("data-expo")

                            link = e.ele("tag:a").link
                            #     link = e.
                            text = e.texts()
                            #     text = e.text
                            data = {
                                "key": key,
                                "title": title,
                                "cat1": cat_1,
                                "cat2": cat_2,
                                "type": "recommend",
                                "url": url,
                                "link": link,
                                "factory_info": text,
                                "json": json,
                            }
                            print(
                                f"add {i} data for cat {cat_1} -{cat_2}-{key} \r {data}"
                            )
                            factoryinranklinkfile.add_data(data)
                            factoryinranklinkdb.add_data(data)
                            # return data
                        except:
                            print(f"{i} we cannot find recommend  data")
                        #     print(faclist[i].inner_html)

                page.close()
                break
            except Exception as e:  # 捕获请求相关的异常
                print(f"Attempt failed with{pro_str} error: {e}")

                if i < max_retries - 1:
                    # time.sleep(2**i)  # 指数退避策略
                    # print("Retrying...")
                    continue  # 继续下一次重试
                else:
                    print("Max retries reached. Exiting without a successful response.")
                    data = {
                        "key": key,
                        "title": title,
                        "cat1": cat_1,
                        "cat2": cat_2,
                        "url": url,
                        "link": "",
                        "factory_info": "",
                    }
                    failed.add_data(data)
                    page.close()
                    break  # 最大重试次数达到，退出循环
        #     page.close()


async def getBangdaninfo(valid_proxies):

    df = pd.read_excel(bangdanpath)
    # df = df.head(2)
    exitingkeys = 0

    if os.path.exists(factoryinranklinkfilepath):
        outdf = pd.read_excel(factoryinranklinkfilepath)
        try:
            exitingkeys = outdf["key"].max()
        except:
            pass
    tasks = []
    # exitingkeys = 2872
    print(f"latest process is {exitingkeys}")
    for key, entry in df.iterrows():
        if key <= exitingkeys:
            print(f"resume from {key}")

            continue
        print(f"do {key}")

        title = entry["bangdan_title"]
        cat_1 = entry["1st_cat"]
        cat_2 = entry["2nd_cat"]
        url = entry["url"]
        # tab = browser.get(url)
        # browser.change_mode()

        task = asyncio.create_task(
            getbangdandetail(key, title, cat_1, cat_2, url, valid_proxies, semaphore)
        )
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    #     for result in results:
    # print(result)

    # Print the results of processing all keywords
    # Wait for any remaining tasks to complete
    if tasks:
        results = await asyncio.gather(*tasks)
        # for result in results:
        #     print(result)


# browser2 = WebPage(chromium_options=co, session_or_options=so)
def getranklinks():
    co = ChromiumOptions().auto_port()
    so = SessionOptions()

    isdowncompany_link = False
    browser = WebPage(chromium_options=co, session_or_options=so)
    urls = [
        "https://sale.1688.com/factory/bd_power_category.html",
        "https://sale.1688.com/factory/bd_hot_category.html",
        "https://sale.1688.com/factory/bd_new_category.html",
        "https://sale.1688.com/factory/bd_serve_category.html",
    ]
    rantitles = ["实力龙头榜", "热度榜", "新晋榜", "服务榜"]
    catlinks = []
    for idx, url in enumerate(urls):
        browser.get(url)
        browser.ele("text=全部").click()

        allcat = browser.eles(".overlay-content-inner-text")
        cattexts = []
        for cat in allcat:

            cat = cat.text
            cattexts.append(cat)
        cattexts = list(set(cattexts))
        # cattexts = ["内衣"]
        for cat in cattexts:

            #     time.sleep(2)
            print(f"click {cat} {rantitles[idx]}")
            if cat == "":
                continue
            currentdict = {"bangdan_title": rantitles[idx], "1st_cat": cat}
            if len(df_dict) > 0 and currentdict in df_dict:
                continue
            browser.refresh()
            browser.ele("text=全部").click()
            time.sleep(2)

            quanbu = browser.ele(".overlay-content-inner")
            try:
                quanbu.ele(f"text={cat}").click()
            except:
                data = {
                    "bangdan_title": rantitles[idx],
                    "bangdan_url": url,
                    "1st_cat": cat,
                    "update": time.strftime("%Y-%m-%d_%H-%M", time.localtime()),
                }
                failed.add_data(data)
                continue

            #     不点击2次 就会出现  元器件分类下面有服装
            #     quanbu.ele(f"text={cat}").click()

            # ismore = False
            # ele = browser.ele("text=查看更多")
            print(f"detect click more:")

            # if ele:
            #     ismore = True
            count = 1
            while True:

                try:
                    ele = browser.ele("text=查看更多")

                    print(f"找到了{count}查看更多")
                    browser.ele("text=查看更多").click()
                    count = count + 1
                    browser.run_js("document.documentElement.scrollTop=1000")
                    time.sleep(5)
                except:
                    print("没有找到。")
                    break
            print(f"grab links:{cat}")
            cats = browser.eles(".factory-rank-card")

            print(f"found {len(cats)}")
            for c in cats:
                try:
                    ranklink = c.ele("tag:a").link
                    title = c.ele(".title-left").text
                    print("2nd", title)
                    data = {
                        "bangdan_title": rantitles[idx],
                        "bangdan_url": url,
                        "1st_cat": cat,
                        "2nd_cat": title,
                        "url": ranklink,
                        "update": time.strftime("%Y-%m-%d_%H-%M", time.localtime()),
                    }
                    ranklinkfile.add_data(data)
                except:
                    print("there is no link for this bangdan")


# GUI线程
bangdanpath = "data/1688-bangdan.xlsx"
ranklinkfile = Recorder(bangdanpath, cache_size=5)
factoryinranklinkdb = DBRecorder(path="data.db", table="fac")

factoryinranklinkfilepath = "data/1688-bangdan-factory.xlsx"
factoryinranklinkfile = Recorder(factoryinranklinkfilepath, cache_size=50)
failed = Recorder("failed.xlsx", cache_size=20)
df_dict = {}
if os.path.exists(bangdanpath):
    df = pd.read_excel(bangdanpath)
    #     df.columns = ["bangdan_title", "1st_cat"]

    #  Step 3: Convert the DataFrame to a dictionary
    df_dict = df[["bangdan_title", "1st_cat"]].to_dict("records")
print(df_dict)

# getranklinks(browser)
# browser.close()
# ranklinkfile.record()
# Run the main function using asyncio.run (ensure this is the main entry point of your script)
if __name__ == "__main__":
    #     # file = Recorder("bestseller-asins.xlsx")
    valid_proxies = []
    if os.path.exists("all_proxies.txt"):
        valid_proxies = open("all_proxies.txt", "r", encoding="utf8").readlines()
    else:
        valid_proxies = open("valid_proxies.txt", "r", encoding="utf8").readlines()
        #     valid_proxies.append(
        #         ["socks5h://" + x for x in open("socks5.txt", "r", encoding="utf8").readlines()]
        #     )

        print(valid_proxies)
        valid_proxies = [v.replace("\n", "") for v in valid_proxies if "\n" in v]
        print("start to clean up proxies")

    if os.path.exists("valid_proxies.txt") == False:
        v = Recorder("valid_proxies.txt")
        v.add_data([v + "\r" for v in valid_proxies])
        v.record()
        with ThreadPoolExecutor(max_workers=100) as executor:
            executor.map(test_proxy, valid_proxies)

        print(f"start to clean up proxies{valid_proxies}")

    asyncio.run(getBangdaninfo(valid_proxies))
    factoryinranklinkfile.record()
    factoryinranklinkdb.record()
    failed.record()
