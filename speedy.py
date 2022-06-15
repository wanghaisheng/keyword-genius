

#!/usr/bin/env python3
# areq.py

"""Asynchronously get links embedded in multiple pages' HMTL."""

import asyncio
import logging
import re
import sys
from typing import IO

import aiofiles
import aiohttp
from aiohttp import ClientSession
from keywordsExpand import get_longtail_keywords_from_one

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger("areq")
logging.getLogger("chardet.charsetprober").disabled = True

HREF_RE = re.compile(r'href="(.*?)"')



async def fetch_one(file: IO, keyword: str, **kwargs) -> None:
    """Write the found HREFs from `keyword` to `file`."""
    res = await get_longtail_keywords_from_one(query=keyword)

    if not res:
        return None
    async with aiofiles.open(file, "a") as f:
        for p in res:
            await f.write(f"{p}\n")
        logger.info("Wrote results for source URL: %s", keyword)

async def bulk_crawl_and_write(file: IO, keywords: set, **kwargs) -> None:
    """Crawl & write concurrently to `file` for multiple `keywords`."""
    async with ClientSession() as session:
        tasks = []
        for keyword in keywords:
            tasks.append(
                fetch_one(file=file, keyword=keyword, session=session, **kwargs)
            )
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    import pathlib
    import sys
    if depth is None:
        depth=1
    assert sys.version_info >= (3, 7), "Script requires Python 3.7+."
    here = pathlib.Path(__file__).parent
    if keywordsinput is None:
        print('there is no intial keywords providing')
        if keywordstxt is None:
            print('there is no intial keywords txt providing')
        else:
            with open(here.joinpath("inputkeywords.txt")) as infile:
                keywords = set(map(str.strip, infile))    
    else:
        keywords=keywordsinput
    for i in range(0,depth):           
        if i >1:
            with open(here.joinpath(str(i-1)+"keywords.txt")) as infile:
                keywords = set(map(str.strip, infile))    
        outpath = here.joinpath(str(i+1)+"keywords.txt")
        with open(outpath, "w") as outfile:
            outfile.write("keywords\n")

        asyncio.run(bulk_crawl_and_write(file=outpath, keywords=keywords))

