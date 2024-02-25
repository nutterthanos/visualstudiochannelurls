import string
import itertools
import asyncio
import aiofiles

URL_PATTERN = "https://aka.ms/vs/15/release/{}/channel"
CHARACTER_SET = string.ascii_lowercase[:6] + string.digits
NUM_CHARACTERS = 9
NUM_URLS_PER_FILE = 10000

async def generate_and_write_urls():
    urls_written = 0
    current_file_number = 1
    current_combination = ('a',) * NUM_CHARACTERS
    current_file_urls = 0
    urls_buffer = []
    
    combinations = itertools.product(CHARACTER_SET, repeat=NUM_CHARACTERS)
    # Advance to the specified combination
    while next(combinations) != current_combination:
        pass
    
    for combination in combinations:
        url = URL_PATTERN.format(''.join(combination))
        urls_buffer.append(url)
        urls_written += 1
        current_file_urls += 1
        
        if current_file_urls >= NUM_URLS_PER_FILE:
            await write_urls_to_file(urls_buffer, current_file_number)
            current_file_number += 1
            current_file_urls = 0
            urls_buffer = []
    
    # Write any remaining URLs to the last file
    if urls_buffer:
        await write_urls_to_file(urls_buffer, current_file_number)
    
    print(f"Total URLs written: {urls_written}")

async def write_urls_to_file(urls_buffer, file_number):
    file_name = f"urls_{file_number}.txt"
    async with aiofiles.open(file_name, "w") as file:
        for url in urls_buffer:
            await file.write(url + "\n")

if __name__ == "__main__":
    asyncio.run(generate_and_write_urls())