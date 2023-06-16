"""
Asynchronous API for data scraping
"""

from __future__ import annotations

import json
import traceback
import warnings
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable, Generic, List, Tuple, Type

if TYPE_CHECKING:
    from _typeshed import SupportsLessThan

import playwright.async_api
from playwright.async_api import Page, Route, TimeoutError, async_playwright
# from pydantic import ValidationError

class TikTokAPIError(Exception):
    """Raised when the API encounters an error"""

    pass


class TikTokAPIWarning(RuntimeWarning):
    pass


class AsyncTikTokAPI():
    """Asynchronous API used to scrape data from TikTok"""

    def __enter__(self):
        raise TikTokAPIError("Must use async context manager with AsyncTikTokAPI")

    async def __aenter__(self) -> AsyncTikTokAPI:
        self._playwright = await async_playwright().start()
        self._browser = await self.playwright.chromium.launch(
            headless=self.headless, **self.kwargs
        )

        context_kwargs = self.context_kwargs

        if self.emulate_mobile:
            context_kwargs.update(self.playwright.devices["iPhone 12"])
        else:
            context_kwargs.update(self.playwright.devices["Desktop Edge"])

        self._context = await self.browser.new_context(**context_kwargs)
        self.context.set_default_navigation_timeout(self.navigation_timeout)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.context.close()
        await self.browser.close()
        await self.playwright.stop()


    async def _scrape_data(
        self,
        link: str,
        scroll_down_time: float = None,
        scroll_down_delay: float = None,
        scroll_down_iter_delay: float = None,
    ):

        if scroll_down_time is None:
            scroll_down_time = 30

        if scroll_down_delay is None:
            scroll_down_delay = 10

        if scroll_down_iter_delay is None:
            scroll_down_iter_delay = 10
        self.navigation_retries=3
        for _ in range(self.navigation_retries + 1):
            # await self.context.clear_cookies()
            page: Page = await self._context.new_page()
#             await page.route("**/api/challenge/item_list/**", capture_api_extras)
#             await page.route("**/api/comment/list/**", capture_api_extras)
#             await page.route("**/api/post/item_list/**", capture_api_extras)
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
            try:
                await page.goto(link, wait_until=None)
                await page.wait_for_selector("#SIGI_STATE", state="attached")
                if self.default_scroll_down_time > 0:
                    await self._scroll_page_down(
                        page,
                        scroll_down_time,
                        scroll_down_delay,
                        scroll_down_iter_delay,
                    )
                # await page.locator("div.sc-hQikvm.vPjhq")
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
                await page.close()
                # data = self._extract_and_dump_data(content, extras_json, data_model)
            except ( IndexError) as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                await page.close()
                continue
            except TimeoutError:
                warnings.warn(
                    "Reached navigation timeout. Retrying...",
                    category=TikTokAPIWarning,
                    stacklevel=2,
                )
                await page.close()
                continue
            break
        else:
            raise TikTokAPIError(
                f"Data scraping unable to complete in {self.navigation_timeout / 1000}s "
                f"(retries: {self.navigation_retries})"
            )

        return data


