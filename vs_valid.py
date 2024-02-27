import aiofiles
import aiohttp
import asyncio
import logging
from aiohttp import ClientSession, ClientResponse

MAX_CONCURRENT_REQUESTS = 4
VALID_URLS_FILE = "valid_urls.txt"
URLS_FILE_PREFIX = "urls_"
URL_PATTERN = "https://aka.ms/vs/15/release/{}/channel"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def fetch(session: ClientSession, url: str, semaphore: asyncio.Semaphore) -> ClientResponse:
    async with semaphore:
        async with session.get(url, allow_redirects=False) as response:
            print(f"Response of {url}, {response}")
            return response

async def process_url(session: ClientSession, url: str, semaphore: asyncio.Semaphore) -> None:
    logger.info(f"Checking url for {url}")
    response = await fetch(session, url, semaphore)
    if "location" in response.headers:
        location = response.headers["location"]
        if "https://download.visualstudio.microsoft.com" in location or "https://download.microsoft.com" in location:
            logger.info(f"Valid URL found: {location}")
            return url  # Return the original aka.ms URL
    return None

async def write_valid_urls(valid_urls):
    async with aiofiles.open(VALID_URLS_FILE, "a") as f:
        for url in valid_urls:
            await f.write(f"{url}\n")
            logger.info(f"Valid URL written to {VALID_URLS_FILE}: {url}")

async def crawl(urls_file: str) -> None:
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    valid_urls = []
    async with aiohttp.ClientSession() as session:
        async with aiofiles.open(urls_file, "r") as f:
            urls = await f.readlines()
            tasks = [process_url(session, url.strip(), semaphore) for url in urls]
            results = await asyncio.gather(*tasks)
            valid_urls += [url for url in results if url is not None]
    await write_valid_urls(valid_urls)

async def main() -> None:
    for i in range(271, 275):  # Updated range to iterate from 271 to 275
        urls_file = f"{URLS_FILE_PREFIX}{i}.txt"
        logger.info(f"Starting crawl for {urls_file}")
        await crawl(urls_file)
        logger.info(f"Finished crawl for {urls_file}")

if __name__ == "__main__":
    asyncio.run(main())
