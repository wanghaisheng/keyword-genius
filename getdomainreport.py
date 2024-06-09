# https://shop.lululemon.com/


# https://sellerdirectories.com/

# https://datarade.ai/data-categories/amazon-sellers-data

# https://brightdata.com/products/datasets/amazon

# https://aimultiple.com/amazon-datasets

# https://viggle.ai/

# bumble.com
# tinder.com

# https://founderbeats.com/
# https://brainimpulse.me/app/tos.html

# clickbank.net

# sites.google.com
# 出站 入站链接


# https://www.healthsupplement24x7.com/


# blog.google


# magnetic chess game kv 6.6k-20.2k  kd 10

# kanoodle game 6，6k 18

# drunk desires card game
# https://drunk-desires.com/


# games for boys 172k 29

# kerplunk game 15.5k 29

# squid game costume
# repack games
# wickedness game
# hook and ring game 6.6k 4
# https://vivereltd.com/

# game of spades perfume 6.6k 19
# fast push game 4.4k 16

# cascadia board game

# best family games 7.7k 28

# best fallout game


# supplement 网站列表
# scrape 所有网站的内容

# 训练


# backlink 出站链接 用这个过滤条件


# stripe.com
# 商业和工业
#  >
# 商业服务
#  >
# 电子商务服务
#  >
# 商户服务和支付系统


# 看看有多少到了支付平台 多少到了联盟营销 比如clickbank.net

# https://zh.trends.fast.wmxpro.com/analytics/backlinks/outbound-domains/?q=SITEs.google.com&searchType=subdomain&ba_category=%2FBusiness%20%26%20Industrial


# 比如这几个就是在sites google建站引流到clickbank的

# https://sites.google.com/view/glucofortorders/
# https://sites.google.com/view/prostasteam2022re/
# https://sites.google.com/view/prostasteam2022re/
# https://sites.google.com/view/lavaslim-france-prix-2024/home

# https://sites.google.com/view/glucofortorders/


# crazytalker.com/recommends/lavaslim-avis/
# mydealsjunction.info/glucofort-buynow
# https://zh.trends.fast.wmxpro.com/analytics/backlinks/refdomains/?q=clickbank.net&searchType=domain&ba_as=%5B0%2C10%5D&ba_mt=new
from playwright.async_api import async_playwright
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio

# from main_backlink_async import get_backlink_munual
# from main_competitors_async import get_domain_competitors
# from main_domaingap_manual import get_domaingap_munual
# from main_domainmagic_manual import get_domainmagic_munual
# from main_organic_async import get_organic_report
# from main_traffic_journey_async import get_traffic_journey
# from main_traffic_analy_async import get_traffic_report
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
from datetime import datetime, timedelta

# Define the semaphore with a limit, for example, 3 concurrent tasks
concurrent_limit = 1
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

    # browser = SessionPage(so)
    browser = WebPage(chromium_options=co, session_or_options=so)

    # browser = WebPage()
    browser.get("https://www.waimaoxia.net/login")
    browser.ele("@placeholder=请输入手机号").input("18926010461")
    browser.ele("@placeholder=请输入登录密码").input("N2mHALSeuR&aG^sN")

    browser.ele(".:geetest_btn_click").click()
    browser.ele(".:login-btn").click()

    return browser


async def get_domain_munual(browser, domain, semaphore, mode=None):
    async with semaphore:  # Acquire the semaphore before starting the task

        tab = browser("Semrush（Trends版）").click.for_new_tab()

        domain = domain.strip()
        if " " in domain:
            domain = domain.replace(" ", "%2520")

        # urls = [
        #     "https://www.trends.fast.wmxpro.com/analytics/traffic/journey/sources?q={domain}",
        #     "https://www.trends.fast.wmxpro.com/analytics/traffic/journey/destinations?q=",
        #     "https://www.trends.fast.wmxpro.com/analytics/traffic/top-pages?device=all_devices&searchType=domain&q=",
        #     "https://www.trends.fast.wmxpro.com/analytics/traffic/subfolders?device=all_devices&searchType=domain&q=",
        #     "https://www.trends.fast.wmxpro.com/analytics/traffic/subdomains?device=all_devices&searchType=domain&q=",
        #     "https://www.trends.fast.wmxpro.com/analytics/organic/positions/?sortField=traffic&sortDirection=desc&db=us&searchType=domain&q=",
        #     "https://www.trends.fast.wmxpro.com/analytics/organic/pages/?sortField=&sortDirection=desc&db=us&searchType=domain&q=",
        #     "https://www.trends.fast.wmxpro.com/analytics/organic/changes/?sortField=&sortDirection=desc&db=us&searchType=domain&q=",
        #     "https://www.trends.fast.wmxpro.com/analytics/organic/competitors/?sortField=&sortDirection=desc&searchType=domain&q=",
        # ]

        urls = [
            f"https://www.trends.fast.wmxpro.com/analytics/traffic/journey/sources?q={domain}",
            f"https://www.trends.fast.wmxpro.com/analytics/traffic/journey/destinations?q={domain}",
            f"https://www.trends.fast.wmxpro.com/analytics/traffic/top-pages?device=all_devices&searchType=domain&q={domain}",
            f"https://www.trends.fast.wmxpro.com/analytics/traffic/subfolders?device=all_devices&searchType=domain&q={domain}",
            f"https://www.trends.fast.wmxpro.com/analytics/traffic/subdomains?device=all_devices&searchType=domain&q={domain}",
            f"https://www.trends.fast.wmxpro.com/analytics/organic/positions/?sortField=traffic&sortDirection=desc&searchType=domain&q={domain}",
            f"https://www.trends.fast.wmxpro.com/analytics/organic/pages/?sortField=&sortDirection=desc&searchType=domain&q={domain}",
            f"https://www.trends.fast.wmxpro.com/analytics/organic/changes/?sortField=&sortDirection=desc&searchType=domain&q={domain}",
            f"https://www.trends.fast.wmxpro.com/analytics/organic/competitors/?sortField=&sortDirection=desc&searchType=domain&q={domain}",
        ]
        modeurls = []
        if mode == None:
            modeurls = urls
        else:
            for url in urls:
                if mode in url:
                    modeurls.append(url)

        current = {"EN": "Current page", "ZH": "当前页面"}
        alllabel = {"EN": "ALL", "ZH": "所有"}

        # 右上角有导出 可以试试 单次能导出3万条 最好根据关键词来
        for idx, url in enumerate(modeurls):
            print(f"start to do {url}----{domain}")

            # url = url + domain
            # tab = browser.new_tab()
            tab.get(url)  # 用标签页对象对标签页进行操作

            locale = tab.ele("@data-test=header_lang_switcher_button").text
            print("locale", locale)
            locale = locale.strip()
            checklocale(tab, locale)

            tab.wait.load_start()
            print("check page counts and records count")
            if "/traffic/top-pages" in url:
                print("here is top-page")

                try:
                    pagecounts = tab.ele("@data-test=pagination").text
                    if "of" in pagecounts:
                        pagecounts = pagecounts.split("of")[-1]
                    if "/" in pagecounts:
                        pagecounts = pagecounts.split("/")[-1]
                    pagecounts = re.sub(
                        r"[^\d]", "", pagecounts
                    )  # \d 匹配一个数字字符，等价于 [0-9]
                    print(f"find pages {pagecounts}:{url}")
                except:
                    # iftab.ele('[data-test="pagination-last"]').is_visible() == False:
                    print("found no pagis ,go next")
                    # continue
                    pagecounts = 0

            elif "/traffic/journey/" in url:
                print("here is journey")

                try:

                    pagecounts = tab.ele("@data-test=pagination-last").text
                    if "of" in pagecounts:
                        pagecounts = pagecounts.split("of")[-1]
                    if "/" in pagecounts:
                        pagecounts = pagecounts.split("/")[-1]
                    pagecounts = re.sub(
                        r"[^\d]", "", pagecounts
                    )  # \d 匹配一个数字字符，等价于 [0-9]
                    print(f"find pages {pagecounts}:{url}")

                except:
                    print("input page no way -found no pagis")
                    # continue
                    # pagecounts = 0
                try:
                    temp = None
                    results = tab.eles("@data-test:tab-total-")
                    print(f"found {len(results)} tab")
                    if "/sources" in url:

                        temp = results[0].text
                    else:
                        temp = results[1].text

                    print(f"RAW PAGECOUNT {pagecounts}")
                    temp = re.sub(
                        r"[^\d]", "", temp
                    )  # \d 匹配一个数字字符，等价于 [0-9]
                    print(f"RAW PAGECOUNT {pagecounts}")

                    pagecounts = temp
                    if int(pagecounts) % 50 == 0:
                        pagecounts = int(pagecounts) / 50
                    else:
                        pagecounts = int(int(pagecounts) / 50) + 1
                        # print("222", pagecounts)
                    print(f"find pages {pagecounts}:{url}")
                except:
                    print("tab result page  way -found no pagis")
                    # continue
                    pagecounts = 0
            elif "/traffic/subfolders" in url or "/traffic/subdomains" in url:
                print("here is subdomain")
                try:
                    if tab.ele("@data-test=pagination"):

                        pagecounts = tab.ele("@data-test=pagination").text
                        if "of" in pagecounts:
                            pagecounts = pagecounts.split("of")[-1]
                        if "/" in pagecounts:
                            pagecounts = pagecounts.split("/")[-1]
                        pagecounts = re.sub(
                            r"[^\d]", "", pagecounts
                        )  # \d 匹配一个数字字符，等价于 [0-9]
                        print(f"find pages {pagecounts}:{url}")
                        # time.sleep(600)
                    else:
                        pagecounts = tab.ele("@data-test=table-total").text
                        print(f"raw pagecounts {pagecounts}")
                        pagecounts = re.sub(
                            r"[^\d]", "", pagecounts
                        )  # \d 匹配一个数字字符，等价于 [0-9]
                        if int(pagecounts) % 50 == 0:
                            pagecounts = int(pagecounts) / 50
                        else:
                            pagecounts = int(int(pagecounts) / 50) + 1
                            # print("222", pagecounts)
                    print(f"find pages {pagecounts}:{url}")
                except:
                    # iftab.ele('[data-test="pagination-last"]').is_visible() == False:
                    print("found no pagis ,go next")
                    pagecounts = 0

                    # continue
            elif "/organic/" in url:
                print("here is organic analystic")
                try:

                    if tab.ele("@data-at=total-pages"):
                        print("here is pagination")

                        pagecounts = tab.ele("@data-at=total-pages").text
                        print(f"RAW PAGECOUNT {pagecounts}")

                        if "of" in pagecounts:
                            pagecounts = pagecounts.split("of")[-1]
                        if "/" in pagecounts:
                            pagecounts = pagecounts.split("/")[-1]
                        pagecounts = re.sub(
                            r"[^\d]", "", pagecounts
                        )  # \d 匹配一个数字字符，等价于 [0-9]
                        print(f"find pages {pagecounts}:{url}")
                        # time.sleep(600)
                    else:
                        print("here is total section")

                        pagecounts = tab.ele("@data-at=total]").text
                        print(f"raw pagecounts {pagecounts}")
                        pagecounts = re.sub(
                            r"[^\d]", "", pagecounts
                        )  # \d 匹配一个数字字符，等价于 [0-9]
                        if int(pagecounts) % 100 == 0:
                            pagecounts = int(pagecounts) / 100
                        else:
                            pagecounts = int(int(pagecounts) / 100) + 1
                            # print("222", pagecounts)
                    print(f"find pages {pagecounts}:{url}")
                except:
                    # iftab.ele('[data-test="pagination-last"]').is_visible() == False:
                    print("found no pagis ,go next")
                    pagecounts = 0
            print("detect table results")
            for no in range(0, int(pagecounts)):
                # for click next

                print(f"start process {domain} page {no}")

                if True:

                    if no == 0:
                        pass
                    else:
                        print(f"you directly go to {domain} {no} page")
                        # time.sleep(lag)

                        try:
                            print(f"start process page {no}")

                            pageurl = url + "&page=" + str(no)
                            tab.get(pageurl)
                            currentpagelocator = None
                            print(f"start check page no {no}")

                            if "/traffic/journey/" in url:
                                currentpagelocator = "@aria-label:Page number"
                            else:
                                currentpagelocator = f"@aria-label={current[locale]}"
                            if tab.ele(currentpagelocator).text != str(no):

                                print(f"sart to fill {domain} page no {no}")

                                tab.ele(currentpagelocator).clear()
                                tab.ele(currentpagelocator).input(str(no))
                                ac = Actions(tab)

                                ac.key_down("ENTER")  # 输入按键名称

                                # tab.ele("@data-ui-name=Pagination.PageInput").input(no)
                                print(f"end to fill {domain} page no {no}")

                            checklocale(tab, locale)

                            tab.wait.load_start()
                            print(f"start check table results {no}")

                            print(f"sleep random {lag}")
                            output = []
                            tabletext = []
                            rowlocator = None
                            celllocator = None
                            if "/traffic/journey/sources" in url:
                                rowlocator = '[data-test="table-row"]'
                                celllocator = "td"
                            elif "/traffic/journey/destinations" in url:
                                rowlocator = '[data-test="table-row"]'
                                celllocator = "td"

                            elif "/top-pages" in url:
                                rowlocator = '[data-test="table-row"]'
                                celllocator = "td"
                            elif "/traffic/subfolders" in url:

                                rowlocator = '[role="row"]'

                                celllocator = "div"
                            elif "/traffic/subdomains" in url:

                                rowlocator = '[role="row"]'
                                # rowlocator = '[data-ui-name="DefinitionTable.Body"] .div'
                                celllocator = "div"
                            elif "/analytics/organic" in url:
                                rowlocator = '[data-test="table-row"]'

                                celllocator = "div"
                            print(f"start check table header {no}")

                            # tabletext = table.eles("@role=row")
                            print("table", tab.ele("@data-test=source-table"))
                            print(tab.ele("@data-test=source-table").ele("tag:thead"))
                            print(tab.ele("@data-test=source-table").ele("tag:tbody"))

                            headers = (
                                tab.ele("@data-test=source-table")
                                .ele("tag:thead")
                                .texts()
                            )
                            print(f"found table headers {headers} for {domain}")
                            data = {
                                "type": mode,
                                "domain": domain,
                                "url": url,
                                "pagecounts": pagecounts,
                                "page": no,
                                "update": time.strftime(
                                    "%Y-%m-%d_%H-%M", time.localtime()
                                ),
                                "lindata": headers,
                            }

                            outfile.add_data(data)
                            print(f"start check table body {no}")

                            table = (
                                tab.ele("@data-test=source-table")
                                .ele("tag:tbody")
                                .children()
                            )
                            if len(table) == 0:
                                break
                            tabletext = table
                            # print("==========", tabletext)
                            print(
                                f"found {domain} {no} table rows",
                                len(tabletext),
                                domain,
                            )
                            tab.change_mode("s")

                            for i in range(0, len(tabletext)):
                                row = tabletext[i]
                                cells = []
                                cells = row.children()

                                lindata = ""
                                print(
                                    f"found  {len(cells)} cells in  table rows {i} for domain {domain}"
                                )
                                browser.set.NoneElement_value("没找到")

                                for j in range(0, len(cells)):
                                    text = None
                                    start_time = datetime.now()
                                    cell = cells[j]
                                    text = cell.raw_text
                                    svgs = cell.eles("tag:svg")
                                    linl = cells.ele("tag:a").link
                                    print("svg", svgs, linl)

                                    # if cells[j].ele("tag:svg"):
                                    #     # else:
                                    #     cdata = []
                                    #     text = ""
                                    #     try:

                                    #         svgs = cells[j].eles("tag:svg")
                                    #         print("this is a icon cell")

                                    #         for e in svgs:
                                    #             cdata.append(e.attr("data-name"))
                                    #         text = "|".join(cdata)
                                    #         try:
                                    #             # if cells[j].ele("tag:a"):
                                    #             print("this is a link cell")
                                    #             text = cells[j].ele("tag:a").link
                                    #         except:
                                    #             pass
                                    #     except:
                                    #         pass

                                    print(f"{j} cell text:{text}")

                                    lindata = lindata + text + ","
                                    end_time = datetime.now()
                                    duration = end_time - start_time
                                    print(
                                        f"{j} costing seconds including days:",
                                        duration.total_seconds(),
                                    )

                                data = {
                                    "type": mode,
                                    "domain": domain,
                                    "url": url,
                                    "pagecounts": pagecounts,
                                    "page": no,
                                    "update": time.strftime(
                                        "%Y-%m-%d_%H-%M", time.localtime()
                                    ),
                                    "lindata": lindata,
                                }

                                outfile.add_data(data)
                                output.append(lindata + "\r")

                            print(f"save {data}  to csv")

                        except:
                            print("retry")
        # outfile.record()
    # print()


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


async def main_domain(domains, modes=[]):
    tasks = []
    browser = getpage()
    domains = list(set(domains))
    for domain in domains:

        domain = domain.replace("https://", "")
        domain = domain.replace("http://", "")

        if "/" in domain:
            domain = domain.replace("/", "")
        if "http:" in domain:
            domain = domain.strip()
        domainName = domain
        if "www." in domainName:
            domainName = domainName.replace("www.", "")
        if domainName.endswith("/"):
            domainName = domainName.rstrip("/")
        if domain:
            for mode in modes:
                task = asyncio.create_task(
                    get_domain_munual(browser, domain, semaphore, mode=mode)
                )
                tasks.append(task)

            # Print the results of processing all domains
        # Wait for any remaining tasks to complete
        if tasks:
            results = await asyncio.gather(*tasks)
            for result in results:
                print(result)


domainmodes = [
    "analytics/traffic/journey/sources",
    "analytics/traffic/journey/destinations",
    "analytics/traffic/top-pages",
    "analytics/traffic/subfolders",
    "analytics/traffic/subdomains",
    "analytics/organic/positions",
    "analytics/organic/pages",
    "analytics/organic/changes",
    "analytics/organic/competitors",
]
# Run the main function using asyncio.run (ensure this is the main entry point of your script)
if __name__ == "__main__":
    # file = Recorder("bestseller-asins.xlsx")
    outfile = Recorder(
        "domains-results" + ".xlsx",
    )

    df = pd.read_csv("domains.csv")

    # domains = pd.read_csv("magic-5w.csv")["domains"].tolist()
    df = df.head(1)
    domains = df["domains"].tolist()

    domainmodes = [
        "analytics/traffic/journey/sources",
        "analytics/traffic/journey/destinations",
        # "analytics/traffic/top-pages",
        # "analytics/traffic/subfolders",
        # "analytics/traffic/subdomains",
        # "analytics/organic/positions",
        # "analytics/organic/pages",
        # "analytics/organic/changes",
        # "analytics/organic/competitors",
    ]
    if domainmodes:
        asyncio.run(main_domain(domains, domainmodes))

    outfile.record()
