from playwright.async_api import async_playwright
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio
import sys
from DataRecorder import Recorder
import pandas as pd
import os, time, random, re
from DrissionPage import (
    ChromiumOptions,
    ChromiumPage,
    SessionPage,
    WebPage,
    SessionOptions,
)
from DrissionPage.common import Keys, Actions
from collections import deque

# Define the semaphore with a limit, for example, 3 concurrent tasks
concurrent_limit = 3
semaphore = asyncio.Semaphore(concurrent_limit)
domains = []


df = pd.read_csv("toolify.csv")
df.columns = df.columns.str.strip()

df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

toolify_domains = df["Website"].tolist()
toolify_domains = list(reversed(toolify_domains))


lag = random.uniform(5, 10)


def checklocale(tab, locale="EN"):
    locator = "@data-test=header_lang_switcher_button"
    if tab.ele(locator).text != locale:

        tab.ele(locator).click()
        try:
            tab.ele("text=English").click()
        except:
            print("cannot click")
        tab.ele(locator).click()
    tab.wait.load_start()


def extract_x(s):
    # Regular expression to match a character followed by itself or twice
    match = re.match(r"(.)\1+", s)
    if match:
        return match.group(1)  # The first captured group is the original character
    else:
        # raise ValueError("The string does not match the expected pattern.")
        return s


def getpage():
    co = ChromiumOptions().auto_port()
    so = SessionOptions()

    browser = WebPage(chromium_options=9225)
    # browser = WebPage()
    browser.get("https://www.waimaoxia.net/login")
    browser.ele("@placeholder=请输入手机号").input("18926010461")
    browser.ele("@placeholder=请输入登录密码").input("N2mHALSeuR&aG^sN")

    browser.ele(".:geetest_btn_click").click()
    browser.ele(".:login-btn").click()

    return browser


def get_backlink_munual(tab):
    print()


async def get_keyword_munual(browser, keyword, semaphore, mode="keywordgap"):
    async with semaphore:  # Acquire the semaphore before starting the task

        tab = browser("Semrush（Trends版）").click.for_new_tab()

        keyword = keyword.strip()
        if " " in keyword:
            keyword = keyword.replace(" ", "%2520")
        if mode == "keywordgap":
            urls = [
                # 0-50  v >1000
                f"https://www.trends.fast.wmxpro.com/analytics/keywordgap/?q=temu.com&searchType=domain&highlightedQuery=etsy.com&protocol=https&keywordType=organic&compareWith=etsy.com%3Adomain%3Aorganic%7Camazon.com%3Adomain%3Aorganic%7Creddit.com%3Adomain%3Aorganic%7Cebay.com%3Adomain%3Aorganic&filter=%257B%2522search%2522%253A%2522{keyword}%2522%252C%2522volume%2522%253A%257B%2522from%2522%253A1000%252C%2522to%2522%253A%2522%2522%257D%252C%2522kd%2522%253A%25220-50%2522%252C%2522intent%2522%253Anull%252C%2522position%2522%253Anull%252C%2522advanced%2522%253A%257B%257D%257D",
                # 0-50 v<1000
                # f"https://www.trends.fast.wmxpro.com/analytics/keywordgap/?q=temu.com&searchType=domain&highlightedQuery=etsy.com&protocol=https&keywordType=organic&compareWith=etsy.com%3Adomain%3Aorganic%7Camazon.com%3Adomain%3Aorganic%7Creddit.com%3Adomain%3Aorganic%7Cebay.com%3Adomain%3Aorganic&filter=%257B%2522search%2522%253A%2522{keyword}%2522%252C%2522volume%2522%253A%257B%2522from%2522%253A%2522%2522%252C%2522to%2522%253A1000%257D%252C%2522kd%2522%253A%25220-50%2522%252C%2522intent%2522%253Anull%252C%2522position%2522%253Anull%252C%2522advanced%2522%253A%257B%257D%257D",
                # if you want sell on q=
                # kd 0-40
                # "https://www.trends.fast.wmxpro.com/analytics/keywordgap/?q=temu.com&searchType=domain&highlightedQuery=etsy.com&protocol=https&keywordType=organic&date=20240517&compareWith=etsy.com%3Adomain%3Aorganic%7Camazon.com%3Adomain%3Aorganic&db=us&filter=%257B%2522search%2522%253Anull%252C%2522volume%2522%253Anull%252C%2522kd%2522%253A%257B%2522from%2522%253A%2522%2522%252C%2522to%2522%253A40%257D%252C%2522intent%2522%253Anull%252C%2522position%2522%253Anull%252C%2522advanced%2522%253A%257B%257D%257D",
                # 41-100 kd
                # 比较每个域名下的数值 如果2个都不是0 则纳入考虑范围
                # "https://www.trends.fast.wmxpro.com/analytics/keywordgap/?q=temu.com&searchType=domain&highlightedQuery=etsy.com&protocol=https&keywordType=organic&date=20240517&compareWith=etsy.com%3Adomain%3Aorganic%7Camazon.com%3Adomain%3Aorganic&db=us&filter=%257B%2522search%2522%253Anull%252C%2522volume%2522%253Anull%252C%2522kd%2522%253A%257B%2522from%2522%253A41%252C%2522to%2522%253A100%257D%252C%2522intent%2522%253Anull%252C%2522position%2522%253Anull%252C%2522advanced%2522%253A%257B%257D%257D",
                # 为啥屏蔽了上面两个，是因为如果不增加其他过滤条件，翻页会太多，根本爬取不了 但可以设置只爬取前20 前100
                # 关键词过滤 比如品类toy with kd 40-100
                # f"https://www.trends.fast.wmxpro.com/analytics/keywordgap/?q=temu.com&searchType=domain&highlightedQuery=etsy.com&protocol=https&keywordType=organic&date=20240517&compareWith=etsy.com%3Adomain%3Aorganic%7Camazon.com%3Adomain%3Aorganic%7Cshein.com%3Adomain%3Aorganic%7Cebay.com%3Adomain%3Aorganic&db=us&filter=%257B%2522search%2522%253A%2522{keyword}%2522%252C%2522volume%2522%253Anull%252C%2522kd%2522%253A%257B%2522from%2522%253A41%252C%2522to%2522%253A100%257D%252C%2522intent%2522%253Anull%252C%2522position%2522%253Anull%252C%2522advanced%2522%253A%257B%257D%257D",
                # supplement with kd 0-50
                # f"https://www.trends.fast.wmxpro.com/analytics/keywordgap/?q=temu.com&searchType=domain&highlightedQuery=etsy.com&protocol=https&keywordType=organic&date=20240517&compareWith=etsy.com%3Adomain%3Aorganic%7Camazon.com%3Adomain%3Aorganic%7Cshein.com%3Adomain%3Aorganic%7Cebay.com%3Adomain%3Aorganic&db=us&filter=%257B%2522search%2522%253A%2522{keyword}%2522%252C%2522volume%2522%253Anull%252C%2522kd%2522%253A%257B%2522from%2522%253A0%252C%2522to%2522%253A50%257D%252C%2522intent%2522%253Anull%252C%2522position%2522%253Anull%252C%2522advanced%2522%253A%257B%257D%257D",
                # 这个方法意味着针对同一类型的产品 找到3-4个竞争对手，就可以通过这些关键词作为与他们差异化的点，比如电商产品
            ]
            filenames = {0: "kd40-100", 1: "kd0-40"}

        if mode == "keywordmagic":

            urls = [
                # 0-50 >1w
                f"https://www.trends.fast.wmxpro.com/analytics/keywordmagic/?protocol=https&filter=H4sIAAAAAAAAA5WPTQoDIQyF75K1CwudjVcZBhGNrZBR8a%2BUYe4%2BTi1dlUKzegkv%2BV420GGNWFxxwUvChgRiXhjoqIcwzlqnK5Vn7zdwvmEqaEBYRRkZhIhJndsgJgZNUUUQfGe%2FrdePdeJ7p8R7UhkHcWjpvKZqUFK4uZ6FM0iYe448XBlTlBZVqX38PdqbMC8noQWqK%2F7xw4X3OjcfIZksdai%2BvI4d37VTqDQBAAA%3D&q={keyword}&type=all&questions=true",
                f"https://www.trends.fast.wmxpro.com/analytics/keywordmagic/?protocol=https&filter=H4sIAAAAAAAAA5WPTQoDIQyF75K1CwudjVcZBhGNrZBR8a%2BUYe4%2BTi1dlUKzegkv%2BV420GGNWFxxwUvChgRiXhjoqIcwzlqnK5Vn7zdwvmEqaEBYRRkZhIhJndsgJgZNUUUQfGe%2FrdePdeJ7p8R7UhkHcWjpvKZqUFK4uZ6FM0iYe448XBlTlBZVqX38PdqbMC8noQWqK%2F7xw4X3OjcfIZksdai%2BvI4d37VTqDQBAAA%3D&q={keyword}&type=all",
                f"https://www.trends.fast.wmxpro.com/analytics/keywordmagic/?protocol=https&filter=H4sIAAAAAAAAA5WPTQoDIQyF75K1CwudjVcZBhGNrZBR8a%2BUYe4%2BTi1dlUKzegkv%2BV420GGNWFxxwUvChgRiXhjoqIcwzlqnK5Vn7zdwvmEqaEBYRRkZhIhJndsgJgZNUUUQfGe%2FrdePdeJ7p8R7UhkHcWjpvKZqUFK4uZ6FM0iYe448XBlTlBZVqX38PdqbMC8noQWqK%2F7xw4X3OjcfIZksdai%2BvI4d37VTqDQBAAA%3D&q={keyword}",
                f"https://www.trends.fast.wmxpro.com/analytics/keywordmagic/?protocol=https&filter=H4sIAAAAAAAAA5WPTQoDIQyF75K1CwudjVcZBhGNrZBR8a%2BUYe4%2BTi1dlUKzegkv%2BV420GGNWFxxwUvChgRiXhjoqIcwzlqnK5Vn7zdwvmEqaEBYRRkZhIhJndsgJgZNUUUQfGe%2FrdePdeJ7p8R7UhkHcWjpvKZqUFK4uZ6FM0iYe448XBlTlBZVqX38PdqbMC8noQWqK%2F7xw4X3OjcfIZksdai%2BvI4d37VTqDQBAAA%3D&q={keyword}&type=phrase",
                f"https://www.trends.fast.wmxpro.com/analytics/keywordmagic/?protocol=https&filter=H4sIAAAAAAAAA5WPTQoDIQyF75K1CwudjVcZBhGNrZBR8a%2BUYe4%2BTi1dlUKzegkv%2BV420GGNWFxxwUvChgRiXhjoqIcwzlqnK5Vn7zdwvmEqaEBYRRkZhIhJndsgJgZNUUUQfGe%2FrdePdeJ7p8R7UhkHcWjpvKZqUFK4uZ6FM0iYe448XBlTlBZVqX38PdqbMC8noQWqK%2F7xw4X3OjcfIZksdai%2BvI4d37VTqDQBAAA%3D&q={keyword}&type=related",
                f"https://www.trends.fast.wmxpro.com/analytics/keywordmagic/?protocol=https&filter=H4sIAAAAAAAAA5WPTQoDIQyF75K1CwudjVcZBhGNrZBR8a%2BUYe4%2BTi1dlUKzegkv%2BV420GGNWFxxwUvChgRiXhjoqIcwzlqnK5Vn7zdwvmEqaEBYRRkZhIhJndsgJgZNUUUQfGe%2FrdePdeJ7p8R7UhkHcWjpvKZqUFK4uZ6FM0iYe448XBlTlBZVqX38PdqbMC8noQWqK%2F7xw4X3OjcfIZksdai%2BvI4d37VTqDQBAAA%3D&q={keyword}&type=exact",
                # 0-50  >5w
                # all
                # f"https://www.trends.fast.wmxpro.com/analytics/keywordmagic/?db=us&protocol=https&filter=H4sIAAAAAAAAA5WPTQoDIQyF75K1CxedjVcZBhGNrZBR8a%2BUYe5eraWrUmhWL%2BEl38sBOuwRiysueEnYkECsGwMd9RTGWet0pfLo%2FQHON0wFDQirKCODEDGpsQ1iYdAUVQTBT%2FbbevlYF352SrwllXESp5bOa6oGJYWr61k4g4S558jTlTFFaVGV2sffo70J6zYILVDd8Y8fFt5rbN5DMlnqUH15HXsCJP%2FuUzQBAAA%3D&q={domain}&type=all",
                # broad 5w
                # "https://www.trends.fast.wmxpro.com/analytics/keywordmagic/?db=us&protocol=https&filter=H4sIAAAAAAAAA5WPTQoDIQyF75K1CxedjVcZBhGNrZBR8a%2BUYe5eraWrUmhWL%2BEl38sBOuwRiysueEnYkECsGwMd9RTGWet0pfLo%2FQHON0wFDQirKCODEDGpsQ1iYdAUVQTBT%2FbbevlYF352SrwllXESp5bOa6oGJYWr61k4g4S558jTlTFFaVGV2sffo70J6zYILVDd8Y8fFt5rbN5DMlnqUH15HXsCJP%2FuUzQBAAA%3D&q=",
                # 0-50 >10w
                # "https://www.trends.fast.wmxpro.com/analytics/keywordmagic/?db=us&protocol=https&filter=H4sIAAAAAAAAA5WPTQoDIQyF75K1CwudjVcZBhGNrZBR8a%2BUMnev1tJVKTSrl%2FCS7%2BUBOuwRiysueEnYkECsGwMd9RTGWet0pXLv%2FQOcb5gKGhBWUUYGIWJSYxvEwqApqgiCH%2By39fyxLvzolHhNKuMkTi2d11QNSgoX17NwBglzz5GnK2OK0qIqtY%2B%2FR3sT1m0QWqC64x8%2FnPiosXoLyWSpQ%2FXlde0JnCNouDUBAAA%3D",
            ]
            kd_urls = [
                # easy
                "https://www.trends.fast.wmxpro.com/analytics/keywordmagic/?db=us&filter=H4sIAAAAAAAAA32OywrCMBBF%2F2XWWajYhfmVUkJIJxqYZkJeIqX%2FbmqKK3F3Z%2BYM565geAmYXXbsFWFFAjlOAkwwPczOWmcK5VebV3C%2BYsw4g7SaEgrggFHv3yAHAVVTQZDnYRP%2F2euXvdy2pgmPqBN2Zc%2FKeUNlRkV8d63MSUDE1IqkTiWMQVnUubT1726HYZx2Q2Uqy2F4cpyTMlx8%2FpzfJ7vguAcBAAA%3D&q=",
                # very easy
                "https://www.trends.fast.wmxpro.com/analytics/keywordmagic/?db=us&filter=H4sIAAAAAAAAA32OSwrDMAwF76K1FymkG18lBGNsuTUolvGvlJK716lDV6W7J2nEvBcY3iIWXzwHRdiQQC6rABPNCNY7502l8uzzC3xomApakE5TRgEcMenjG%2BRVQNNUEeS0i%2F%2Fo%2FEUv894t8Z50xmEcWflgqFpUxDffu0wCEubeIw8qY4rKoS61r39XOw3LehgaU91Ow4OTzcpwDeVzfgO%2FVDE8BgEAAA%3D%3D&q=",
                # possible
                "https://www.trends.fast.wmxpro.com/analytics/keywordmagic/?db=us&filter=H4sIAAAAAAAAA32OSwrDMAwF76K1F4Gmi%2FoqIRjjyK1BsYx%2FpYTcvU4duirdPUkj5m1geA2YXXbsFWFFAjnNAkwwPSzOWmcK5VebN3C%2BYsy4gLSaEgrggFEf3yCvAqqmgiAvwy7%2Bs%2BOXHW9704RH1Am7smflvKGyoCK%2Bu1ZmEBAxtSKpUwljUBZ1Lm39u9tpmObDUJnKehqeHJekDBefP%2Bc3upwrvwcBAAA%3D&q=",
                # difficult
                "https://www.trends.fast.wmxpro.com/analytics/keywordmagic/?db=us&&filter=H4sIAAAAAAAAA32OSwrDMAwF76K1F1m0heYqIRhjy61AsY1%2FpYTcPU4duirdjaQn5q2g%2FRIwUybvJGNFhnGaBeigOxiylnTh%2FG7zCuQqxowGRqs4oQAfMKrjG8argKq4YKNhE%2F%2Bzl2%2F2dt%2BaJjyjStiVnSU5zcWgZP%2BgVmYQEDG1IqmnEsYgLapc2vp3t9MwzYehei7LaXj5aJLUvrj8Oe8Vz8lCBwEAAA%3D%3D&q=",
                # hard
                "https://www.trends.fast.wmxpro.com/analytics/keywordmagic/?db=us&filter=H4sIAAAAAAAAA32OSwrDMAwF76K1F1mktPgqIRjjyK1BsYx%2FpYTcvU4duirdPUkj5m1geA2YXXbsFWFFAjnNAkwwPSzOWmcK5VebN3C%2BYsy4gLSaEgrggFEf3yAvAqqmgiCvwy7%2Bs%2BOXvY1704RH1Am7smflvKGyoCK%2Bu1ZmEBAxtSKpUwljUBZ1Lm39u9tpmObDUJnKehqeHJekDBefP%2Bc3hEjZ7AcBAAA%3D&q=",
                # very hard
                "https://www.trends.fast.wmxpro.com/analytics/keywordmagic/?db=us&filter=H4sIAAAAAAAAA32OywrDIBBF%2F2XWLiw0UPyVEER0bIWJiq9SQv69poauSnd3Zs5w7gY6rBGLKy54SdiQQMwLAx31CMZZ63Sl8urzBs43TAUNCKsoI4MQManjG8TEoCmqCOI27ew%2Fe%2F2yF8737omPpDIO58jSeU3VoKRwd70NZ5Aw9yZ5UBlTlBZVqX39u9ypmJfD0ALV9TQ8QzJZ6lB9%2BZzfWaeSZggBAAA%3D&q=",
            ]
            filenames = {
                0: "easy",
                1: "very-easy",
                2: "possible",
                3: "difficult",
                4: "hard",
                5: "very-hard",
            }

        current = {"EN": "Current page", "ZH": "当前页面"}
        alllabel = {"EN": "ALL", "ZH": "所有"}

        # 右上角有导出 可以试试 单次能导出3万条 最好根据关键词来
        for idx, url in enumerate(urls):
            print(f"start to do {url}----{keyword}")

            # url = url + domain
            # tab = browser.new_tab()
            tab.get(url)  # 用标签页对象对标签页进行操作

            if tab.ele(".sm-table-error"):
                print("reach daily limit,please try tomorrow")
                tab.close()
                browser.quit()
                raise Exception
            locale = tab.ele("@data-test=header_lang_switcher_button").text
            print("locale", locale)
            locale = locale.strip()
            checklocale(tab, locale)

            tab.wait.load_start()
            pagecounts = 0
            print("start to check pagecounts")
            try:

                tab.wait.load_start()
                # print("check counts")
                pagecounts = tab.ele("@data-testid=all-keywords").text
                print("all keywords count", pagecounts)

                if "," in pagecounts:
                    pagecounts = pagecounts.replace(",", "")

                #     #     # 这里需要确保pagecounts是整数
                if int(pagecounts) % 100 == 0:
                    pagecounts = int(pagecounts) / 100
                else:
                    pagecounts = int(int(pagecounts) / 100) + 1
                    # print("222", pagecounts)

                print(f"find {keyword} pages {pagecounts}:{url}")

            except:
                if mode == "keywordgap":
                    # print("choose all mode")
                    # tab.ele("@data-at=table-keyword-type-pill-total").click()
                    # allmode = tab.ele("@data-at=table-keyword-type-pill-total")

                    pagecounts = tab.ele("@data-at=pill-volume").attr("aria-label")
                    # print("choose all", pagecounts)
                    # time.sleep(600)
                    if alllabel[locale] in pagecounts:
                        pagecounts = pagecounts.replace(alllabel[locale], "")
                    if "," in pagecounts:
                        pagecounts = pagecounts.replace(",", "")

                    #     #     # 这里需要确保pagecounts是整数
                    if int(pagecounts) % 100 == 0:
                        pagecounts = int(pagecounts) / 100
                    else:
                        pagecounts = int(int(pagecounts) / 100) + 1
                        # print("222", pagecounts)

                    print(f"find {keyword} pages {pagecounts}:{url}")
                if mode == "keywordmagic":
                    pagecounts = tab.ele("@data-ui-name=Pagination.TotalPages").text
                    print("check keywordmagic page count", pagecounts)

                    print(f"find pages {pagecounts}:{url}")

            if pagecounts == 0:
                print("found no pagis ,go next")

                continue

            lines = []

            for no in range(1, int(pagecounts) + 1):
                # for click next

                print(f"start process {keyword} page {no}")
                if "keywordgap" in url:
                    path = "keywordgap"
                elif "keywordmagic" in url:
                    path = "keywordmagic"
                else:
                    path = "other"

                if os.path.exists(path) == False:
                    os.mkdir(path)
                if os.path.exists(path + os.sep + keyword) == False:
                    os.mkdir(path + os.sep + keyword)
                if True:

                    if no == 1:
                        pass
                    else:
                        print(f"you directly go to {keyword} {no} page")
                        # time.sleep(lag)

                        try:

                            print(f"sart to fill {keyword} page no {no}")

                            tab.ele(f"@aria-label={current[locale]}").clear()
                            tab.ele(f"@aria-label={current[locale]}").input(str(no))
                            ac = Actions(tab)

                            ac.key_down("ENTER")  # 输入按键名称

                            # tab.ele("@data-ui-name=Pagination.PageInput").input(no)
                            print(f"end to fill {keyword} page no {no}")

                            # checklocale(tab, locale)

                            tab.wait.load_start()
                        except:
                            print("retry")

                    # tab.change_mode("s")
                    print("start to save table to disk")
                    try:
                        output = []
                        tabletext = []
                        headers = []
                        if "keywordgap" in url:

                            table = (
                                tab.ele("#keywordsTable")
                                .ele("@data-ui-name=DefinitionTable.Body")
                                .children()
                            )
                            if len(table) == 0:
                                break
                            tabletext = table
                            # tabletext = table.eles("@role=row")
                            headers = (
                                tab.ele("#keywordsTable")
                                .ele("@data-ui-name=DefinitionTable.Head")
                                .texts()
                            )
                            print(f"detect headers:{headers}")
                            data = {
                                "type": mode,
                                "keyword": keyword,
                                "url": url,
                                "pagecounts": pagecounts,
                                "page": no,
                                "update": time.strftime(
                                    "%Y-%m-%d_%H-%M", time.localtime()
                                ),
                            }
                            if len(headers) > 0:
                                for key in headers:
                                    data[key] = ""
                            print(f"add header:{data}")
                            outfile.add_data(data)
                        elif "keywordmagic" in url:

                            headers = tab.ele("@data-testid=table-header-row").texts()
                            print(f"detect headers:{headers}")
                            headers.remove("PKD %")
                            data = {
                                "type": mode,
                                "keyword": keyword,
                                "url": url,
                                "pagecounts": pagecounts,
                                "page": no,
                                "update": time.strftime(
                                    "%Y-%m-%d_%H-%M", time.localtime()
                                ),
                            }
                            if len(headers) > 0:
                                for key in headers:
                                    if key == "PKD %":
                                        continue
                                    data[key] = ""
                            print(f"add header:{data}")
                            outfile.add_data(data)
                            tabletext = tab.eles("@data-testid=table-row")
                            if len(tabletext) == 0:
                                break
                        # print("==========", tabletext)
                        print(
                            f"found {keyword} {no} table rows",
                            len(tabletext),
                            keyword,
                        )

                        for i in range(0, len(tabletext)):
                            lined = tabletext[i]
                            c1 = []
                            rowdata = lined.texts()
                            print(
                                f"found  {len(rowdata)} cells for  table rows {i} for keyword {keyword}"
                            )
                            print(f"row list {rowdata}")

                            data = {
                                "type": mode,
                                "keyword": keyword,
                                "url": url,
                                "pagecounts": pagecounts,
                                "page": no,
                                "update": time.strftime(
                                    "%Y-%m-%d_%H-%M", time.localtime()
                                ),
                                # "lindata": rowdata,
                            }
                            print(
                                "start to match header and value",
                                len(headers),
                                len(rowdata),
                            )
                            if len(headers) == len(rowdata):
                                result_dict = {k: v for k, v in zip(headers, rowdata)}
                                # print(result_dict)
                                for (
                                    k
                                ) in (
                                    result_dict
                                ):  # Iterate over the keys of result_dict
                                    data[k] = result_dict[
                                        k
                                    ]  # Assign the value from result_dict to the
                            try:
                                polylinedata = (
                                    tab.ele(".sm-cell-trend__chart")
                                    .ele("tag:polyline")
                                    .attr("points")
                                )
                                data["趋势"] = polylinedata

                                data["趋势类型"] = gettrendtype(polylinedata)
                            except:
                                pass

                            print(f"add data:{data}")
                            outfile.add_data(data)

                        print(f"save {keyword}  page {no} result to csv")
                    except:
                        print("it seemed reach daily limits")
                        break
            # outfile.record()
        tab.close()
    # print()


def gettrendtype(path_data):
    from svgpathtools import parse_path

    try:
        # 定义SVG路径数据
        # path_data = "M 0,4.23 L 3.27,6.78 L 6.55,4.23 L 9.82,6.78 L 13.09,6.78 L 16.36,4.23 L 19.64,4.23 L 22.91,4.23 L 26.18,4.23 L 29.45,6.78 L 32.73,4.23 L 36,4.23"
        path = parse_path(path_data)

        # 初始化斜率总和
        total_slope = 0
        # 线段计数
        segment_count = 0
        slopes = []

        # 遍历路径中的每个段，计算斜率
        for i, segment in enumerate(path):
            if i == 0:  # 跳过第一个moveto命令
                continue
            start_point = path[i - 1].start
            end_point = segment.end
            dx = end_point.real - start_point.real
            dy = end_point.imag - start_point.imag
            if dx != 0:  # 避免除以零
                slope = dy / dx
                total_slope += slope
                segment_count += 1
                slopes.append(slope)

        # 计算平均斜率
        average_slope = total_slope / segment_count

        # 根据平均斜率判断整体趋势
        trend_type = 1 if abs(average_slope) < 0.1 else 2 if average_slope > 0 else 3

        # 输出整体趋势类型编号
        #         1: 保持平稳
        # 2: 逐渐增大
        # 3: 逐渐减小
        #         如果平均斜率接近零，我们可以认为整体趋势是保持平稳。
        # 如果平均斜率是正数，我们可以认为整体趋势是逐渐增大。
        # 如果平均斜率是负数，我们可以认为整体趋势是逐渐减小。
        print(f"Overall Trend Type: {trend_type}")
        if trend_type == 2:
            trend_type = detect_up_trend(slopes, average_slope)
        return trend_type

    except:
        return 4


# 检测趋势类型
def detect_up_trend(slopes, avg_slope):
    trend_type = 1 if abs(avg_slope) < 0.1 else 2 if avg_slope > 0 else 3
    sudden_increase_threshold = 0.1  # 突变阈值
    duration_threshold = 3  # 持续时间阈值
    sudden_increase = None

    # 查找是否存在突变点
    for i in range(1, len(slopes)):
        if abs(slopes[i] - slopes[i - 1]) > sudden_increase_threshold:
            sudden_increase = i
            break

    # 如果存在突变点，检查是否符合趋势类型
    if sudden_increase is not None:
        if trend_type == 2:  # 逐渐增大
            # 检查突变后是否保持增高或持续增高
            if all(
                slope >= slopes[sudden_increase]
                for slope in slopes[
                    sudden_increase : sudden_increase + duration_threshold
                ]
            ):
                trend_type = "第二种：突变后保持增高或持续增高"
                trend_type = 2.1
            else:
                trend_type = 2.2
                trend_type = "第一种：突变后保持一段时间然后回落"
    return trend_type


# Function to rename subfolder if it exists
def rename_subfolder(base_path, old_name, new_name):
    old_folder_path = os.path.join(base_path, old_name)
    new_folder_path = os.path.join(base_path, new_name)

    if os.path.exists(old_folder_path):  # Check if the old folder exists
        if not os.path.exists(
            new_folder_path
        ):  # Check if the new folder name doesn't already exist
            os.rename(old_folder_path, new_folder_path)  # Rename the folder
            print(f"Renamed '{old_name}' to '{new_name}'")
        else:
            print(f"A folder named '{new_name}' already exists. Skipping renaming.")
    else:
        print(f"No folder named '{old_name}' found. Skipping renaming.")


def renamedomainfolder():
    for domain in toolify_domains:
        if "https://" in domain:
            domain = domain.replace("https://", "")
        if "http://" in domain:
            domain = domain.replace("http://", "")
        if "www." in domain:
            domain = domain.replace("www.", "")

        if len(domain.split(".")) == 2:
            domainName = domain.split(".")[0]
        elif len(domain.split(".")) == 1:
            domainName = domain.split(".")[0]
        elif len(domain.split(".")) > 2:
            domainName = domain.split(".")[1]
        rename_subfolder("", domainName, domain)


async def main_keywords(keywords, mode):
    # Initialize the Playwright asynchronous context manager
    # Create an asyncio event loop
    # page = await getpage(playwright=playwright)
    tasks = []
    browser = getpage()
    keywords = list(set(keywords))
    done_keywords = []
    if os.path.exists(outpath):
        df = pd.read_excel(outpath)

        done_keywords = df["keyword"].tolist()

    for keyword in keywords:
        keyword = keyword.strip()
        if keyword and keyword not in done_keywords:
            task = asyncio.create_task(
                get_keyword_munual(browser, keyword, semaphore, mode=mode)
            )
            tasks.append(task)

        # task = asyncio.create_task(
        #     get_keywordmagic_munual(playwright, domain, keyword)
        # )
        # tasks.append(task)
        # Print the results of processing all keywords
    # Wait for any remaining tasks to complete

    try:
        # 等待所有任务完成
        if tasks:
            results = await asyncio.gather(*tasks)
            for result in results:
                print(result)

    except asyncio.CancelledError:
        # 处理任务被取消的情况
        print("Tasks were cancelled")
    except Exception as e:
        # 处理其他所有异常
        print(f"An exception occurred: {e}")
        sys.exit(1)  # 根据情况可能需要重新抛出 SystemExit 或者退出程序
    finally:
        # 清理工作
        pass


keywords = []
# Run the main function using asyncio.run (ensure this is the main entry point of your script)
if __name__ == "__main__":
    # file = Recorder("bestseller-asins.xlsx")
    outfile = None
    outpath = None

    mode = 2
    # get keyword total number to auto set filter:search volumn
    if mode == 1:
        df = pd.read_csv("gap.csv")
        # df = df.head(1)
        keywords = df["keywords"].tolist()
        keywords = list(set(keywords))
        outpath = "keywords-keywordgap-results"

        outfile = Recorder(
            outpath + ".xlsx",
        )
        asyncio.run(main_keywords(keywords, "keywordgap"))

    else:
        df = pd.read_csv("magic.csv")
        # df = df.head(1)
        keywords = df["keywords"].tolist()
        keywords = list(set(keywords))

        outpath = "keywords-keywordmagic-results"
        outfile = Recorder(
            outpath + ".xlsx",
        )
        asyncio.run(main_keywords(keywords, "keywordmagic"))

    outfile.record()
