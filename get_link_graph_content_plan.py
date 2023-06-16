import asyncio


import asyncio

import botright


async def main():
    botright_client = await botright.Botright(headless=False)
    browser = await botright_client.new_browser()
    page = await browser.new_page()
    await page.add_init_script(
                """
if (navigator.webdriver === false) {
    // Post Chrome 89.0.4339.0 and already good
} else if (navigator.webdriver === undefined) {
    // Pre Chrome 89.0.4339.0 and already good
} else {
    // Pre Chrome 88.0.4291.0 and needs patching
    delete Object.getPrototypeOf(navigator).webdriver
}
            """
            )
    # Continue by using the Page
    url ="https://dashboard.linkgraph.com/content/content-planner/3946af54-e8f1-4f9b-b72f-5b79e6bc5e0e"
    await page.goto(url, wait_until=None)
    data=[]

    for li in await page.get_by_role('sc-hQikvm.vPjhq').all():
        commercial=await li.get_by_role('sc-kxCoLp.gfrvgX').text_content()
        kd=await li.get_by_role('sc-futMm gGEFEd').text_content()
        keywords=li.locator('div.sc-eZgkGA.cxUAlk div').text_content()
        d ={
            'type':commercial,
            "kd":kd,
            "keywords":keywords
        }
        data.append(d)
    print(data)
    await botright_client.close()

if __name__ == "__main__":
    asyncio.run(main())