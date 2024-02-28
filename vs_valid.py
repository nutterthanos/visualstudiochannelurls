import aiofiles
import aiohttp
import asyncio
import logging
import time
from aiohttp import ClientSession, ClientResponse

MAX_CONCURRENT_REQUESTS = 2
VALID_URLS_FILE = "valid_urls.txt"
URLS_FILE_PREFIX = "urls_"
URL_PATTERN = "https://aka.ms/vs/15/release/{}/channel"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def fetch(session: ClientSession, url: str, semaphore: asyncio.Semaphore) -> ClientResponse:
    async with semaphore:
        async with session.get(url, allow_redirects=False) as response:
            logger.info(f"Response of {url}, {response.status}")
            return response

async def process_url(session: ClientSession, url: str, semaphore: asyncio.Semaphore) -> None:
    logger.info(f"Checking url for {url}")
    response = await fetch(session, url, semaphore)
    if response.status not in [302, 200]:  # Check if status code is not 302 or 200
        return url  # Return the url if it encountered a non-302, non-200 error
    elif "location" in response.headers:
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

async def crawl(urls_file: str, failed_urls: list) -> None:
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    valid_urls = []
    new_failed_urls = []
    async with aiohttp.ClientSession() as session:
        async with aiofiles.open(urls_file, "r") as f:
            urls = await f.readlines()
            tasks = [process_url(session, url.strip(), semaphore) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result, url in zip(results, urls):
                if isinstance(result, str):  # If the result is a URL (i.e., a non-302, non-200 error occurred)
                    failed_urls.append(url.strip())  # Add the failed URL to the list
                elif result is not None:
                    valid_urls.append(result)  # Append valid URLs
                else:
                    if url.strip() in failed_urls:
                        logger.info(f"URL {url.strip()} is now valid (status 302 or 200), removing from failed URLs")
                    else:
                        logger.error(f"Unexpected result for URL {url.strip()}")
    await write_valid_urls(valid_urls)
    return failed_urls

async def main() -> None:
    failed_urls = []
    for i in range(81, 85):  # Updated range to iterate from 81 to 85
        urls_file = f"{URLS_FILE_PREFIX}{i}.txt"
        logger.info(f"Starting crawl for {urls_file}")
        failed_urls = await crawl(urls_file, failed_urls)
        if failed_urls:
            logger.info(f"Pausing for 30 seconds due to non-302, non-200 HTTP status codes")
            time.sleep(30)  # Sleep for 30 seconds
            logger.info(f"Retrying failed URLs after pausing")
    logger.info(f"Finished crawl for all files")

if __name__ == "__main__":
    asyncio.run(main())
