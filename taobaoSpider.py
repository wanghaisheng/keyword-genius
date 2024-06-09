import json
import csv
import sys
import time
import random
import tkinter
from selenium import webdriver
from selenium.webdriver.common.by import By
from threading import Thread
from playsound import playsound
import re
import traceback
from DrissionPage import ChromiumOptions, ChromiumPage, SessionPage, WebPage

from DataRecorder import Recorder

VERSION = "1.1"
print(
    f"程序版本{VERSION}\n最新程序下载地址:https://github.com/zhangjiancong/MarketSpider"
)

# 全局变量状态文字
gui_text = {}
gui_label_now = {}
gui_label_eta = {}

# 淘宝页面版本 0旧 1新
tbPageVersion = 0


# GUI函数
def guiFunc():
    global gui_text
    global gui_label_now
    global gui_label_eta
    gui = tkinter.Tk()
    gui.title("淘宝店铺信息爬取器 Powered by zjc")
    gui["background"] = "#ffffff"
    gui.geometry("600x100-50+20")
    gui.attributes("-topmost", 1)
    gui_text = tkinter.Label(gui, text="初始化", font=("微软雅黑", "20"))
    gui_text.pack()
    gui_label_now = tkinter.Label(gui, text="?", font=("微软雅黑", "10"))
    gui_label_now.pack()
    gui_label_eta = tkinter.Label(gui, text="?", font=("微软雅黑", "10"))
    gui_label_eta.pack()
    gui.mainloop()


# GUI线程控制
Gui_thread = Thread(target=guiFunc, daemon=True)
Gui_thread.start()
time.sleep(2)

# 启动浏览器
gui_text["text"] = "☞等待搜索关键词"
gui_text["background"] = "#f35315"
keyword = input("输入搜索关键词:")
gui_text["background"] = "#ffffff"
gui_text["text"] = "正在启动浏览器"


co = ChromiumOptions().auto_port()
browser = WebPage()

#
browser.get("https://www.taobao.com")
gui_text["background"] = "#ffffff"

# CSV相关
csvfile = Recorder(
    f'{keyword}_taobao_{time.strftime("%Y-%m-%d_%H-%M", time.localtime())}.csv',
    cache_size=48,
    # "a",
    # encoding="utf-8-sig",
    # newline="",
)


# cookie相关
gui_text["text"] = "正在清空Cookie"
# browser.delete_all_cookies()
gui_text["text"] = "正在注入Cookie"

try:
    cookie = "mtop_partitioned_detect=1; _m_h5_tk=9cd91ec7382adcfea459145f29d4939e_1716646564373; _m_h5_tk_enc=e9bc106663bfccb89e6cf5217e016d27; thw=xx; t=afbb32b22e96fa60f7fb0bc7e8424e4f; _tb_token_=e9be3f56b9653; cna=TMDYHrz9KQ0BASQJinCLubq2; xlly_s=1; _samesite_flag_=true; 3PcFlag=1716638286905; cookie2=1932738f401d5fd8da5fb4d19b0b8ae0; unb=41027104; lgc=whs860603; cancelledSubSites=empty; cookie17=Vy0T5%2B8VwJc%3D; dnk=whs860603; tracknick=whs860603; _l_g_=Ug%3D%3D; sg=340; _nk_=whs860603; cookie1=BdWOhrGtepTIf1Azf41ZeKhvu3%2BVKqF5wJAUP2A5gFg%3D; sgcookie=E100wPT1jWda%2FxqoSCaZW88g42SFznaUcV0lcOYbKc0sgHKMkI5eaqBqotunVGlHw6v8rH7aG2b1v96a7CwoCTy0uvZayv0bIY7AUGXHpU34mnm6Ei%2Fai%2BPZbs%2B%2B6Iw%2B5ARC; havana_lgc2_0=eyJoaWQiOjQxMDI3MTA0LCJzZyI6IjQ3M2MzYzQ4MmQ1M2RlYjcwN2NlZTc3NGE1MjM2Mjk2Iiwic2l0ZSI6MCwidG9rZW4iOiIxZFlUZ1hZcUhsUXBCbXpaZ1FXVDk2QSJ9; _hvn_lgc_=0; havana_lgc_exp=1715824392106; cookie3_bak=1932738f401d5fd8da5fb4d19b0b8ae0; cookie3_bak_exp=1716897526699; wk_cookie2=15bfabb53999d08992520cde4eb4fb68; wk_unb=Vy0T5%2B8VwJc%3D; uc1=existShop=false&cookie21=Vq8l%2BKCLiv0MyZ1zjQnMQw%3D%3D&cookie16=U%2BGCWk%2F74Mx5tgzv3dWpnhjPaQ%3D%3D&pas=0&cookie14=UoYfp3Lr5sGOUA%3D%3D&cookie15=V32FPkk%2Fw0dUvg%3D%3D; sn=; uc3=vt3=F8dD3eK3UX8HnVmKCGw%3D&nk2=FPGrO6YOp14x&id2=Vy0T5%2B8VwJc%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D; csg=44a39691; env_bak=FM%2BgnE2ezWFFZE6ZmO7yAfZz4cX7PptRhpCsQaMkEtWy; skt=0f2307ab760a661c; existShop=MTcxNjYzODMyNg%3D%3D; uc4=nk4=0%40FnomOfgAKR2S2zXqVResREtMRa0%3D&id4=0%40VXqdFBXDpx7mkBK88dP3a0fo3g%3D%3D; _cc_=WqG3DMC9EA%3D%3D; JSESSIONID=E20278EBE94C64F9B9D07C490934E508; tfstk=fdsE9dsAVkEEVhQk_Cty_CDVU_-pmnFbYgOWETXkdBAHOTvk41f7pB6u9_SysTQQpUNKUvINg0iQ9yBo43tuGSZbc9BB23VfsLE6RXp2K0qWrBxgOAxzfSZbc94Hp36gG8Lpl_OkF3vH-2vgQppxr3YHqC2wELGnrDflIRJJspvkqDYMjK9-t4cHWHx_bLL39qe-f7kjGedcKBXCdGXrGIWHs0mlcp8el9AZq0jNWMDXUB4xCQKB9TpFwonpxU7hTdxz4cxF99jk7gN_ceWDE_KCj80Hiw1BjMbqE0XwYBY5vehU_IjdIiKM5o2VIGCCpGWSEuv1GCXdx3r0HH-HthJOV5nHaNblAeK-tW-lQLjyLbpirqIR8b0y-dpwGRyiNVoKhHWL05g-yeBvQIwnK43J-KpwGRyqy4LpHdRbLS5..; isg=BIWF-hZmT1UhOWsJJdyfYy7qlMG_QjnUkgzO4YfqCbzLHqSQT5DlpPR0KELoNlGM"
    # with open("taobao.cookie", "r") as f:
    # cookie_list = json.load(f)
    browser.set.cookies(cookie)

    # for cookie in cookie_list:
    # browser.add_cookie(cookie)
except:
    print("未找到Cookie")
gui_text["text"] = "正在刷新浏览器"
browser.refresh()
# 搜索词与页数获取
gui_text["text"] = "正在操作"
browser.get(f"https://s.taobao.com/search?q={keyword}")

# browser.implicitly_wait(10)
try:
    # 老版PC淘宝页面
    taobaoPage = browser.ele(
        "#J_relative > div.sort-row > div > div.pager > ul > li:nth-child(2)"
    ).text
    taobaoPage = re.findall("[^/]*$", taobaoPage)[0]
    tbPageVersion = 0
except:
    # 新版PC淘宝页面
    taobaoPage = browser.ele(
        ".next-pagination-display",
    ).text
    print(taobaoPage)
    taobaoPage = taobaoPage.split("/")[-1]
    # taobaoPage = re.findall("[^/]*$", taobaoPage)[-1]
    tbPageVersion = 1
# page1.ele("@placeholder=Enter keyword").input(keyword)

# # 点击登录按钮
# page1.ele("text=Check keyword").click()
# kd = page1.ele(".css-16bvajg-chartValue").text

# kds = page1.ele(".css-1wi5h2-row css-1crciv5 css-6rbp9c").text
# 爬取页数控制
gui_text["text"] = "☞等待爬取页数"
gui_text["background"] = "#f35315"
print(f"共计{taobaoPage}页,建议每2小时总计爬取不超过20页")
page_start = int(input("起始页数："))
page_end = int(input("截止页数：")) + 1
gui_text["background"] = "#ffffff"

for page in range(page_start, page_end):
    gui_text["text"] = f"当前正在获取第{page}页，还有{page_end - page_start - page}页"
    gui_text["bg"] = "#10d269"
    gui_label_now["text"] = "-"
    gui_label_eta["text"] = "-"
    browser.get(
        f"https://s.taobao.com/search?q={keyword}&page={page}&_input_charset=utf-8&commend=all&search_type=item&source=suggest&sourceId=tb.index"
    )

    if browser.title == "验证码拦截":
        gui_text["text"] = f"出错：如有验证请验证。等待20秒"
        gui_text["bg"] = "red"
        gui_label_eta["text"] = "-"
        gui_label_now["text"] = f"-"
        playsound("error.wav")
        time.sleep(20)
    time.sleep(1)
    # 尝试获取商品列表
    # 等待页面加载
    browser.wait.load_start()
    # 切换到收发数据包模式
    # browser.change_mode()

    try:
        gui_text["text"] = (
            f"当前正在获取第{page}页，还有{page_end - page_start - page}页"
        )
        gui_text["bg"] = "#10d269"
        goods_arr = (
            browser(
                "@data-spm=item",
            )
            .child()
            .children()
        )
        goods_length = len(goods_arr)
        print(f"found {goods_length} goods")
        for i, goods in enumerate(goods_arr):
            try:
                i = i + 1
                # browser.run_js("document.documentElement.scrollTop=1000")
                gui_label_now["text"] = f"正在获取第{i}个,共计{goods_length}个"
                if goods.texts() is None:
                    print(f"ignore this {i}")
                    continue

                item_name = goods.ele(".^Title").text

                item_price_int = goods.ele(
                    ".^Price--priceInt",
                ).text

                item_price_float = goods.ele(
                    ".^Price--priceFloat",
                ).text
                item_price = item_price_int + item_price_float
                print(goods.eles(".^Price--procity")[0].text)
                price_pro = goods.eles(".^Price--procity")[0].text
                price_city = goods.eles(".^Price--procity")[0].text

                print(item_price)
                # time.sleep(6000)
                try:
                    ads = goods.ele(".^SalesPoint--iconPic").attr("src")
                    if (
                        ads
                        == "https://gw.alicdn.com/tfs/TB108qKrbH1gK0jSZFwXXc7aXXa-60-36.png"
                    ):
                        ads = 1
                    else:
                        ads = 0
                except:
                    ads = 0
                try:
                    item_mainpic = goods.ele(".^MainPic--mainPic").attr("src")
                except:
                    item_mainpic = ""
                item_shop = goods.ele(".^ShopInfo--shopName").text
                shop_link = goods.ele(".^ShopInfo--shopName").attr("href")
                # href="//store.taobao.com/shop/view_shop.htm?spm=a21n57.1.2.1.5d71523c99kswv&appUid=RAzN8HWZPt7BtcqyLD8phAozGqERur2tGT27qBtxJyLHgA8SDBr"
                item_link = goods.ele(".^Card--doubleCardWrapper").attr("href")

                # href = "//detail.tmall.com/item.htm?priceTId=2150425e17166399338625486e374b&id=520880796002&ns=1&abbucket=6"
                item_paid = goods.ele(".^Price--realSales").text
                try:
                    b = shop_link.split(
                        "https://store.taobao.com/shop/view_shop.htm?appUid="
                    )[1]
                except:
                    b = shop_link
                data = {
                    "no": i + (i - 1) * 48,
                    "item_name": item_name,
                    "ads": ads,
                    "pro": price_pro,
                    "city": price_city,
                    "item_mainpic": item_mainpic,
                    "item_price": item_price,
                    "item_shop": item_shop,
                    "shop_link": shop_link,
                    "item_link": item_link,
                    "bridge": b,
                    "item_paid": item_paid,
                }
                csvfile.add_data(data)
            except:
                print(f"第{i}个商品获取信息出错,跳过")
                traceback.print_exc()
    except Exception as e:
        print(f"在遍历商品时出错{e}")
        traceback.print_exc()
        # 拉取商品列表失败则提示需要验证
        gui_text["text"] = f"出错：如有验证请验证。等待20秒"
        gui_text["bg"] = "red"
        gui_label_eta["text"] = "-"
        gui_label_now["text"] = f"注意:第<{page}>页将跳过如需获取请重新运行程序！"
        print(f"注意:第<{page}>页将跳过如需获取请重新运行程序！")
        playsound("error.wav")
        time.sleep(5)
    print("page relau")
    delay_time = random.randint(1, 5)
    for delay in range(delay_time):
        gui_label_now["text"] = "-"
        gui_text["bg"] = "#eeeeee"
        gui_text["text"] = f"第{page}页，还有{page_end - page_start - page}页"
        gui_label_eta["text"] = f"延时翻页：已延时{delay}秒，剩余{delay_time}秒"
        time.sleep(10)

print("程序结束")
gui_text["text"] = "程序结束正在保存文件"
csvfile.record()
gui_text["text"] = "保存文件完成，准备退出中"
time.sleep(5)
browser.close()
sys.exit()
