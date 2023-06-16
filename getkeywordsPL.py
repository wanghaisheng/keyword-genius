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
from pydantic import ValidationError

class TikTokAPIError(Exception):
    """Raised when the API encounters an error"""

    pass


class TikTokAPIWarning(RuntimeWarning):
    pass


class AsyncTikTokAPI(TikTokAPI):
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

    async def _extract_and_dump_data(
        self, page_content: str, extras_json: List[dict], data_model: Type[]
    ):
        data = page_content.split('<script id="SIGI_STATE" type="application/json">')[
            1
        ].split("</script>")[0]

        if self.data_dump_file:
            with open(
                f"{self.data_dump_file}.{data_model.__name__}.json",
                "w+",
                encoding="utf-8",
            ) as f:
                j = json.loads(data)
                j["extras"] = extras_json
                json.dump(j, f, indent=2)

        parsed = data_model.parse_raw(data)
        if isinstance(parsed, MobileResponseMixin):
            parsed = parsed.to_desktop()
        return parsed

    async def _scrape_data(
        self,
        link: str,
        data_model: Type[],
        scroll_down_time: float = None,
        scroll_down_delay: float = None,
        scroll_down_iter_delay: float = None,
    ) -> Tuple[_DataModelT, List[APIResponse]]:

        if scroll_down_time is None:
            scroll_down_time = self.default_scroll_down_time

        if scroll_down_delay is None:
            scroll_down_delay = self.default_scroll_down_delay

        if scroll_down_iter_delay is None:
            scroll_down_iter_delay = self.default_scroll_down_iter_delay

        api_extras: List[APIResponse] = []
        extras_json: List[dict] = []

        async def capture_api_extras(route: Route):
            try:
                await route.continue_()
                response = await route.request.response()
            except playwright.async_api.Error:
                return

            if not response:
                return

            try:
                _data = await response.json()
            except json.JSONDecodeError:
                return

            extras_json.append(_data)
            api_response = APIResponse.parse_obj(_data)
            api_extras.append(api_response)

        for _ in range(self.navigation_retries + 1):
            await self.context.clear_cookies()
#             page: Page = await self._context.new_page()
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
                await page.locator("#search-form-google-keyword-md")
                if self.default_scroll_down_time > 0:
                    await self._scroll_page_down(
                        page,
                        scroll_down_time,
                        scroll_down_delay,
                        scroll_down_iter_delay,
                    )

                content = await page.content()
                await page.close()

                data = self._extract_and_dump_data(content, extras_json, data_model)
            except (ValidationError, IndexError) as e:
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

        return data, api_extras
t= AsyncTikTokAPI()
t._scrape_data('https://keywordtool.io/')

