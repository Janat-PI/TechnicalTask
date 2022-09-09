import asyncio
from playwright.async_api import async_playwright, Page


async def text(page: Page):
    result = await page.inner_text()
    print(result)


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        url = "https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273?ad=offering"
        pag = await page.goto(url)
        # print(await page.title())
        await text(pag)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())