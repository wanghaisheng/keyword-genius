import os.path

from functions.marketSpider import *
import sys
import time
import random
import tkinter
from threading import Thread
import logging
import os
from DrissionPage import (
    ChromiumOptions,
    ChromiumPage,
    SessionPage,
    WebPage,
    SessionOptions,
)

from DataRecorder import Recorder


def mknewdir(dirname):
    if not os.path.exists(f"{dirname}"):
        nowdir = os.getcwd()
        os.mkdir(nowdir + f"\\{dirname}")


VERSION = "1.0"
print(
    f"程序版本{VERSION}\n最新程序下载地址:https://github.com/zhangjiancong/MarketSpider"
)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
mknewdir("logs")
file_handler = logging.FileHandler(
    os.path.join("./logs", "1688.log"), mode="a+", encoding="utf-8"
)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s - Line:%(lineno)d - %(levelname)s - %(message)s"
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.info("start")

# 全局GUI文字
status = tkinter.Label()
label1 = tkinter.Label()
label2 = tkinter.Label()


def gui_loop():
    global status
    global label1
    global label2
    root = tkinter.Tk()
    root.title("1688店铺信息获取器 Powered by zjc")
    root["background"] = "#ffffff"
    root.geometry("600x100-50+20")
    root.attributes("-topmost", 1)
    status = tkinter.Label(root, text="初始化", font=("微软雅黑", "20"), bg="#ffffff")
    status.pack()
    label1 = tkinter.Label(root, text="-", font=("微软雅黑", "10"), bg="#ffffff")
    label2 = tkinter.Label(root, text="-", font=("微软雅黑", "10"), bg="#ffffff")
    label1.pack()
    label2.pack()
    root.mainloop()


def write_statue(showtext, bgcolor="#ffffff"):
    status["text"] = showtext
    if bgcolor == "green":
        status["bg"] = "#00f400"
        return 1
    if bgcolor == "red":
        status["bg"] = "red"
        return 1
    status["bg"] = bgcolor
    status["text"] = showtext
    return 0


def write_label(label1text="-", label2text="-"):
    label1["text"] = label1text
    label2["text"] = label2text


csvfile = None


def run(keywords, modeno, browser):
    write_statue("☞等待搜索关键词", "#ffff99")
    modes = ["所有选项", "所有货源", "找工厂", "找供应商", "工业品"]

    modetext = modes[int(modeno)]

    # keywords = input("输入搜索关键词:")
    # logger.info(f"get keyword={keywords}")
    csvfile = Recorder(
        f"data/{keywords}_{modetext}_1688.xlsx",
        cache_size=30,
        # "a",
        # encoding="utf-8-sig",
        # newline="",
    )

    try:
        # with open("taobao.cookie", "r") as f:
        # cookie_list = json.load(f)
        browser.get("https://s.1688.com/selloffer/offer_search.htm")
        print("scan qr code to login")
        time.sleep(30)
        cookie_list = browser.cookies(as_dict=False, all_domains=True)
        # for cookie in cookie_list:
        # print(cookie)
        # browser.add_cookie(cookie)
    except:
        print("未找到Cookie")

    write_statue("启动浏览器中")
    browser.get("https://s.1688.com/selloffer/offer_search.htm")
    write_statue("尝试添加Cookie")

    # browser.set.cookies()
    write_statue("搜索商品中")
    try:
        cap = browser.ele("text:请拖动下方滑块完成验证").texts()
        print("ccap", cap)
        if cap:
            print("there is captcha here")
            size = browser.ele(".nc_wrapper").rect.corners[2]
            browser.ele(".nc_iconfont btn_slide").drag_to(size)
            # time.sleep(60)
    except:
        print("no capcha at all")
    browser.ele(f"text={modetext}").click()
    browser.ele("#alisearch-input").input(keywords)
    browser.ele("#alisearch-input").click()

    note = Recorder("data/" + keywords + "-" + modetext + "-note.txt")

    try:
        sugge = browser.ele(".suggest_left_list").texts()

        note.add_data(sugge)
        note.add_data("================\r")
    except:
        print(f"there is no auto suggestions {keywords}")
    browser.ele("text=搜 索").click()
    time.sleep(1)

    if modeno == 1:
        biaoqian = browser.eles(".sn-item-row")
        for i in range(len(biaoqian)):
            print(biaoqian[i].text)
            note.add_data(biaoqian[i].text)

    elif modeno == 2:
        fenlei = browser.eles(".sn-item-col")
        for i in range(len(fenlei)):

            print(fenlei[i].text)
            note.add_data(fenlei[i].text)
        cities = browser.eles(".sn-item-col city-item-col")
        for i in range(len(cities)):
            note.add_data(cities[i].text)

            print(cities[i].text)
    elif modeno == 3:
        biaoqian = browser.eles(".:sm-sn-items-count-a")
        for i in range(len(biaoqian)):
            print(biaoqian[i].text)
            note.add_data(biaoqian[i].text)

    note.record()
    getPage = browser.ele(".fui-paging-num").text
    write_statue("☞等待获取页数", "#ffff99")
    write_label(f"已找到{getPage}页", "输入起始页和终点页")
    print(f"已找到{getPage}页，请按照提示输入页数")
    logger.info(f"get 1688 {modetext} for {keywords} have pages {getPage}")
    # try:
    #     StartPage = int(input("起始页数:"))
    #     EndPage = int(input("截止页数:")) + 1
    # except:
    #     StartPage = 1
    #     EndPage = int(getPage) + 1
    StartPage = 1
    df = None

    if os.path.exists(f"{keywords}_{modetext}_1688.xlsx"):
        import pandas as pd

        df = pd.read_excel(f"{keywords}_{modetext}_1688.xlsx")
        StartPage = df["page"].max()
        print(f"已记录{getPage}页，从该页数开始抓取")

    EndPage = int(getPage) + 1
    logger.info(f"get startPage{StartPage};get EndPage{EndPage - 1}")
    searchUrl = browser.url
    exitSignal = False
    for page in range(StartPage, EndPage):
        if os.path.exists(f"{keywords}_{modetext}_1688.xlsx"):
            import pandas as pd

            df = pd.read_excel(f"{keywords}_{modetext}_1688.xlsx")

        write_statue(f"当前正在获取第{page}页，还有{EndPage - page}", "green")
        write_label()
        if page != 1:
            # https://s.1688.com/company/pc/factory_search.htm?keywords=fda&spm=a26352.24780423.searchbox.input&beginPage=2#sm-filtbar
            # browser.get(searchUrl + f"&beginPage={page}#sm-filtbar")
            browser.ele(".space-common-pagination").ele("tag:input").clear()
            browser.ele(".space-common-pagination").ele("tag:input").input(page)
            time.sleep(1)
            browser.ele(".fui-paging-btn fui-btn").click()
            # browser.ele("text=:确定").click()
            browser.wait.load_start()

            # browser.change_mode()
            try:
                cap = browser.ele("text:亲，请拖动下方滑块完成验证").text
                if cap:
                    print("there is captcha here")
                    size = browser.ele(".nc_wrapper").rect.corners[2]
                    browser.ele(".nc_iconfont btn_slide").drag_to(size)
                    # time.sleep(60)
            except:
                print("no capcha at all")
            for i in range(1, 5):

                browser.run_js("document.documentElement.scrollTop=100000")
                time.sleep(3)

        # for i in range(1, 5):
        #     browser.scroll_page()
        #     time.sleep(3)
        # 等待页面加载
        browser.wait.load_start()
        # 切换到收发数据包模式
        # browser.change_mode()
        try:
            locator = None
            if int(modeno) in [1, 4]:
                print("find all products")
                locator = ".space-offer-card-box"
            else:
                print("find all company")

                locator = ".company-offer-contain"
            goods_arr = browser.eles(locator)
            print(f"page {page}found products", len(goods_arr))
            # for item in goods_arr:
            # print(item(".title").text)

            goods_length = len(goods_arr)
        except:
            try:
                notifimsg = browser.ele("text:没找到相关的商品").text
                if notifimsg == "没找到相关的商品":
                    write_statue(f"{page}页开始无商品，程序退出", "red")
                    print(f"{page}页进入无相关商品页面，退出")
                    logger.critical(
                        f"fail get goods in page{page},return cannot found goods,exit"
                    )
                    exitSignal = True
                    break
            except:
                pass
            write_statue(f"出错：如有验证请验证。程序暂停30秒可供自由操作", "red")
            write_label(f"注意：第{page}页获取将跳过，请重新运行获取该页！")
            print(f"获取{modetext}列表出错")
            logger.warning(
                f"catch a error in page{page},maybe need to Captcha,this page will be jumped"
            )
            time.sleep(30)
            continue
        if exitSignal == True:
            break
        namelist = []
        for num, goods in enumerate(goods_arr):
            browser.change_mode()
            raw = goods.texts()[0]
            # num = num + 1

            if raw is None:
                print(f"ignore this {num}")
                continue
            if "\n" in raw:
                raw = raw.replace("\n", ",")
            if df is not None:
                if raw in df["raw"].tolist():
                    print("item already there")
                    continue

            try:
                write_statue(
                    f"当前正在获取第{page}页，还有{EndPage - StartPage - page}页",
                    "green",
                )
                write_label(f"正在获取第{num}个，共计{goods_length}个")
                if modeno == 1:
                    try:
                        item_name = goods.ele(".title").text
                    except:
                        item_name = ""
                    item_price = goods.ele(".showPricec").text
                    # print(item_price)
                    try:
                        item_pic = (
                            goods.ele(".mojar-element-title")
                            .ele("tag:a")
                            .ele("tag:img")
                            .attr("src")
                        )
                    except:
                        item_pic = (
                            goods.ele(".mojar-element-image")
                            .ele("tag:a")
                            .ele("tag:img")
                            .attr("src")
                        )
                    # print(item_pic)
                    item_sale = goods.ele(".sale").text
                    if item_sale == "":
                        item_sale = 0
                    # print(item_sale)
                    item_offer_tag = goods.ele(".offer-tags").text
                    print(item_offer_tag)
                    try:
                        item_repurchase_rate = goods.ele(".shop-repurchase-rate").text
                    except:
                        item_repurchase_rate = 0
                    item_shop = goods.ele(".company-name").attr("title")

                    shop_link = goods.ele(".company-name").child().attr("href")
                    item_link = (
                        goods.ele(".mojar-element-title").ele("tag:a").attr("href")
                    )
                    data = {
                        "id": num,
                        "page": page,
                        "item_name": item_name,
                        "item_price": item_price,
                        "item_sale": item_sale,
                        "item_offer_tag": item_offer_tag,
                        "item_repurchase_rate": item_repurchase_rate,
                        "item_shop": item_shop,
                        "shop_link": shop_link,
                        "item_link": item_link,
                        "item_pic": item_pic,
                        "raw": raw,
                        "update": time.strftime("%Y-%m-%d_%H-%M", time.localtime()),
                    }
                    # print(data)
                    csvfile.add_data(data)

                elif modeno in [2, 3]:
                    # print(num, "======", goods.texts())
                    try:
                        company_img = (
                            goods.ele(".img-container").ele("tag:div").attr("style")
                        )
                        if company_img:
                            company_img = company_img.replace(
                                'background-image: url("', ""
                            )
                            company_img = company_img.replace('"', "")
                    except:
                        company_img = ""
                    # print(company_img)
                    try:
                        company_name = goods.ele(".title-container").ele(".title").text
                    except:
                        company_name = ""
                    # print(company_name)
                    if company_name in namelist:
                        break
                    try:
                        company_city = goods.ele(".location").text
                    # print(company_city)
                    except:
                        company_city = ""
                    try:
                        company_identity = goods.ele(".identity-tag").text
                    # print(company_identity)
                    except:
                        company_identity = ""
                    try:
                        company_desc = goods.ele(".desc").text
                    # print(company_desc)
                    except:
                        company_desc = ""
                    try:
                        company_rate = goods.ele(".rate-container").text
                    # print(company_rate)
                    except:
                        company_rate = ""
                    try:
                        company_tags = goods.ele("@data-btrack-clkpos=工厂标签").text
                    # print(company_tags)
                    except:
                        company_tags = ""
                    # print(company_link)
                    baseurl = "https://sale.1688.com/factory/card.html?memberId="
                    companyid = ""
                    try:
                        company_link = goods.ele(".:space-factory-card").attr(
                            "data-gokey"
                        )
                        # 广告位的class是
                        # <div class="space-factory-card is-ad"
                        # print("link", company_link)
                        if "^item_id@" in company_link:
                            t = company_link.split("^item_id@")[-1]
                            if "^" in t:
                                companyid = t.split("^")[0]
                                company_link = baseurl + companyid
                    except:
                        print("company link weired")
                        company_link = ""
                    # page_id@DnCbnkkfcL4Q6PSL4FdzrtDVxJNB8uUKMs0LSfq0GbmFQ5FJ^pageId@DnCbnkkfcL4Q6PSL4FdzrtDVxJNB8uUKMs0LSfq0GbmFQ5FJ^request_id@4ynJS8KrQ6B2MFcH5HZjsYDWAbpxBAs6FcD1716719163964^fe_abtest_ids@^fe_abtest_buckets@^fe_abtest_bucket_index@^fe_abtestinfo@^se_keyword@hg^item_id@b2b-2207268045985a7cdc^object_type@factory^qualification@strength^is_super_factory_all@1^fac_tag@anXinOffer^type@offer^position@16^sp_expo_data@scene^TPP;fab^484480_472461_479601_2517456_481130_439754_455011_468820_441597_2489781_441611_2492835_441612_441613_2489783_441614_452344_2491749_441615_441616_465832_476952_469637_441870_460928_432633_468254_440368_460692_2520207_2491258_456112_441890_2491597_2491772_463347_482051_482050_482052_463862_443562_468433_441532_2491260_451907_466758_468406_2486431_2490229_2490264_469270_2485920_2492140_2486589_465424_2491871_449102_2508966_482454_460657_2515374_446697_450438_2519759_2518465_2518467_2506109_2495831_459002_2492458_455080_2508667_2515404_2495856_2516567_2507554_2516347_2516731_436598_453326_469853_466120_476743_448169_476901_463786_2492436_2492835_2492758_2495843_2495966_2483743_2485829_2485833_2485836_2485839_2485842_2485846_2485850_2485920_2485947_2485955_2486431_2486589_2486622_2487257_2508271_2500064_2504424_2505519_2505807_2506723_2510164_2508955_2508735_2508966_2509119_2510469_2509680_2510157_2511076_2511380_2514246_2514794_2515092_2515095_2516352_2516772_2516760_2488309_2517322_2518745_2517905_2517909_2517904_2489783_2489781_2490264_2490229_481130_2520207_2520929_2520936_2520941_2521195_2491260_2491258_2491749_2492140_2491321_2491527_2491597_2491772_2491871_2492406_2492766_2495199_2492406_2497760_2498309_2499523_2508909_2515165_2516796_2521015_2521024_2521029_2521766_2522694_2514230;qp^2492436%232492835%232492758%232495843%232495966%232483743%232485829%232485833%232485836%232485839%232485842%232485846%232485850%232485920%232485947%232485955%232486431%232486589%232486622%232487257%232508271%232500064%232504424%232505519%232505807%232506723%232510164%232508955%232508735%232508966%232509119%232510469%232509680%232510157%232511076%232511380%232514246%232514794%232515092%232515095%232516352%232516772%232516760%232488309%232517322%232518745%232517905%232517909%232517904%232489783%232489781%232490264%232490229%23481130%232520207%232520929%232520936%232520941%232521195%232491260%232491258%232491749%232492140%232491321%232491527%232491597%232491772%232491871;qrwMode^0;offerId^712921049396;rankId^712921049396;facGroup^2;facRankScore^13439212544;facZgcDeepCtr^0.0309559;facZgcDeepCvr^;facSmallScore^0.0007192;facHuopanScore^0.0000000;facReleAgent^0.0000000;facReleDomin^0.0000000;facReleHuopan^0.0000000;facReleJgname^0.0000000;facReleQpconf^0.0000000;facReleRegion^0.0000000;facReleZycate^0.0000000;facReleWeekend^0.0000000;facReleFlowControl^0.0000000;facReleText^2.0000000;facReleSuper^0.0000000;facReleRetarget^0.0000000;facReleTBRetarget^0.0000000;facAxgScore^0.0000000;facCrossScore^0.0000000;facCateGmvScore^0.0000000;facRetargetScore^0.0000000;offerGroup^1.0000000;offerSmallScore^0.0037814;searchType^main_search;query^hg;opense^2492406%3B2492766%3B2495199%3B2492406%3B2497760%3B2498309%3B2499523%3B2508909%3B2515165%3B2516796%3B2521015%3B2521024%3B2521029%3B2521766%3B2522694%3B2514230;recallType^normal%2C;
                    data = {
                        "id": num,
                        "page": page,
                        "companyid": companyid,
                        "company_name": company_name,
                        "company_city": company_city,
                        "company_identity": company_identity,
                        "company_desc": company_desc,
                        "company_rate": company_rate,
                        "company_tags": company_tags,
                        "company_link": company_link,
                        "company_img": company_img,
                        "raw": raw,
                        "baseinfo": "",
                        "pc_card_exhibition": "",
                        "ability_info": "",
                        "imgs": [],
                        "catlog": [],
                        "update": time.strftime("%Y-%m-%d_%H-%M", time.localtime()),
                    }
                    print("get company detail")
                    if isdowncompany_link and company_link:
                        # furl = "https://sale.1688.com/factory/card.html?memberId="
                        try:
                            c_detail = browser.new_tab(company_link)
                            # 获取第二个标签页对象
                            # c_detail = browser.get_tab(c_detail)
                            baseinfo = c_detail.ele("#pc_card_baseinfo").texts()
                            data["baseinfo"] = baseinfo
                            pc_card_exhibition = c_detail.ele(
                                "#pc_card_exhibition"
                            ).texts()
                            data["pc_card_exhibition"] = pc_card_exhibition
                            data["ability_info"] = [
                                x.texts() for x in c_detail.eles(".ability_info")
                            ]
                            data["imgs"] = [
                                x.link
                                for x in c_detail.eles("@src^https://cbu01.alicdn.com/")
                            ]
                            c_detail.close()
                        except:
                            c_detail.close()

                        # pc - card - exhibition_cooperation=c_detail.ele('@data-btrack:pc-card-exhibition-cooperation').text
                        # https://sale.1688.com/factory/card.html?memberId=b2b-2207268045985a7cdc
                        print("get product catlog")

                        cbase = "https://sale.1688.com/sale/zgc/scene/9h84vd49.html?spm=a262cb.19918180.ljxo5qvc.1.556b1a99Pl0NWG&__pageId__=229310&cms_id=229310&facMemId="
                        try:
                            catlog = browser.new_tab(cbase + companyid)
                            c_items = catlog.eles(".galleyItemLink")
                            if len(c_items) > 0:
                                items = []
                                try:
                                    for item in c_items:
                                        img = item.ele(".galleyImg").link
                                        title = item.ele(".basicInfobox").text
                                        tag = item.ele(".tagsLine").text
                                        price = item.ele(".customDetails").text
                                        items.append(
                                            {
                                                "title": title,
                                                "tag": tag,
                                                "price": price,
                                                "imgs": img,
                                            }
                                        )
                                    data["catlog"] = items

                                except:
                                    print("catlog parse error")
                            catlog.close()

                        except:
                            catlog.close()
                        print(num, "========", data)
                    namelist.append(company_name)
                    csvfile.add_data(data)

            except:
                logger.warning(f"get item{num} in page{page} failed,jump this goods")
                write_statue(f"出错：如有验证请验证。程序暂停5秒可供自由操作", "red")
                write_label(f"item{num} in page{page}广告类商品或未知属性商品过滤")
                print(f"item{num} in page{page}广告类商品或未知属性商品过滤")
                time.sleep(5)
                continue

        if page == EndPage:
            break

        delay_time = random.randint(5, 10)
        for delay in range(delay_time):
            write_statue(
                f"已获取第{page}页，还有{EndPage - StartPage - page}页", "#ffffff"
            )
            write_label(
                "当前正在随机延时翻页", f"已延时{delay}秒，剩余{delay_time - delay}秒"
            )
            time.sleep(1)
    csvfile.record()

    return browser


klist = [
    "无麸质",
    "fda",
    "小单定制",
    "可开授权",
    "专利",
    "外贸",
    "雷达波",
    "复古",
    "西藏",
    "麻将",
    "道教",
    "太极",
    "刮痧",
    "穿戴",
    "中医",
    "gmp",
    "红外",
    "保健品",
    "红光",
    "生肖",
    "熊猫",
    "创意",
    "驱蚊",
    "3d",
    "3d立体拼图",
    "益智",
    "孔明锁",
    "鲁班锁",
    "榉木",
    "整蛊",
    "拼装模型",
    "改装件",
    "app",
    "游艇",
    "磁吸",
    "隐形",
    "巧克力",
    "药食同源",
    "沙发",
]


# 如果是找工厂，pc端最多有151页
# 通过构造url的方式 100页以后的都无法访问 会停留在100页
# https://s.1688.com/company/pc/factory_search.htm?keywords=%B9%CE%F0%F0&spm=a26352.13672862.searchbox.input&beginPage=101#sm-filtbar
# import asyncio


# async def main(klist):
#     # Initialize the Playwright asynchronous context manager
#     # Create an asyncio event loop
#     co = ChromiumOptions().auto_port()
#     so = SessionOptions()

#     tasks = []
#     for i in klist:


#         browser = WebPage(chromium_options=co, session_or_options=so)
#         browser2 = WebPage(chromium_options=co, session_or_options=so)

#         if len(tasks) >= 2:  # If we have 3 tasks already, wait for them to complete
#             results = await asyncio.gather(*tasks)
#             for result in results:
#                 print(result)
#             tasks.clear()  # Clear the list of tasks

#         task = asyncio.create_task(run(i, 2, browser))
#         tasks.append(task)
#         task = asyncio.create_task(run(i, 3, browser2))
#         tasks.append(task)

# Print the results of processing all keywords
# # Wait for any remaining tasks to complete
# if tasks:
#     results = await asyncio.gather(*tasks)
#     for result in results:
# print(result)

# GUI线程

co = ChromiumOptions().auto_port()
so = SessionOptions()
isdowncompany_link = True
browser = WebPage(chromium_options=co, session_or_options=so)
# browser2 = WebPage(chromium_options=co, session_or_options=so)
for no in range(0, len(klist), 1):
    # modeno = input('输入模式对应数字 1"所有货源", 2"找工厂", 3"找供应商", 4"工业品"')

    # Thread(target=run, args=(keywords, 2, browser)).start()
    # Thread(target=run, args=(keywords, 3, browser2)).start()
    # time.sleep(60)
    Gui_thread = Thread(target=gui_loop)
    Gui_thread.setDaemon(True)
    Gui_thread.start()
    time.sleep(3)
    run(klist[no], 2, browser)
    # run(klist[no + 1], 2, browser)
    # run(klist[no + 2], 2, browser)
    # run(klist[no + 3], 2, browser)

    # modeno = 2
    # if os.path.exists(keywords + "_找工厂_1688.xlsx"):
    #     pass
    # else:
    #     run(keywords, modeno, browser)
    #     # Thread(target=run, args=(keywords, 2, browser)).start()
    # modeno = 3

    # if os.path.exists(keywords + "_找供应商_1688.xlsx"):
    # pass
    # else:
    # run(keywords, modeno, browser)
    # Thread(target=run, args=(keywords, 3, browser2)).start()

# # 新建2个页面对象，自动分配端口的配置对象能共用，但指定端口的不可以
# page1 = ChromiumPage(co)
# page2 = ChromiumPage(co)
# # 第一个浏览器访问第一个网址
# page1.get("https://gitee.com/explore/ai")
# # 第二个浏览器访问另一个网址
# page2.get("https://gitee.com/explore/machine-learning")

# # 新建记录器对象
# recorder = Recorder("data.csv")

# # 多线程同时处理多个页面
# Thread(target=collect, args=(page1, recorder, "ai")).start()
# Thread(target=collect, args=(page2, recorder, "机器学习")).start()

print("程序结束")
logger.info("exit")

write_statue("程序结束，正在保存文件")
browser.close()

write_statue("保存结束，准备退出")
time.sleep(5)
sys.exit(0)
# Run the main function using asyncio.run (ensure this is the main entry point of your script)
# if __name__ == "__main__":
#     # file = Recorder("bestseller-asins.xlsx")

#     asyncio.run(main(klist))
#     # file.record()
