import asyncio
import traceback
from random import randint

from playwright.async_api import async_playwright, Locator, Browser, Page

import bot
import config
import database
import time_utils
from config import URL_LIST, UrlConfig


async def get_alpha(canvas: Locator) -> int:
    alpha = await canvas.evaluate("""
    canvas => {
        const ctx = canvas.getContext('2d');
        if (!ctx) return null;

        const x = Math.floor(canvas.width / 2);
        const y = Math.floor(canvas.height / 2);

        const pixel = ctx.getImageData(x, y, 1, 1).data;
        return pixel[3]; // alpha
    }
    """)
    return int(alpha)


BROWSER: Browser


async def open_page(url: str) -> Page:
    global BROWSER
    page = await BROWSER.new_page()
    await page.goto(url)
    return page


class Lot:
    def __init__(self, preview: str, url: str, title: str, cost: str, id: int, is_wyroznione: bool, location: str, date: str):
        self._desc = None
        self._preview = preview
        self.url = url
        self.title = title
        self.cost = cost
        self.id = id
        self.is_wyroznione = is_wyroznione
        self.location = location
        self.date = date

    @staticmethod
    async def create(locator: Locator):
        url = 'https://www.olx.pl' + await locator.locator('div>div>div>a').first.get_attribute('href')
        title = await locator.locator('a>h4').first.text_content()
        cost = await locator.locator('div[data-cy=ad-card-title]>p').first.text_content()
        id = int(await locator.get_attribute('id'))
        is_wyroznione = await get_alpha(locator.locator('canvas')) > 0
        data = (await locator.locator('p[data-testid=location-date]').text_content()).split(' - ')
        location = data[0]
        date = data[1]
        preview = await locator.locator('img').first.get_attribute('src')
        return Lot(preview, url, title, cost, id, is_wyroznione, location, date)

    async def description(self):
        if self._desc:
            return self._desc
        try:
            page = await open_page(self.url)
            self._desc = await page.locator('div[data-cy="ad_description"]>div').inner_html(timeout=5000)
            await page.close()
        except:
            self._desc = "Not provided"

        return self._desc

    async def preview(self):
        return self._preview

    def __str__(self):
        return f'[{self.id} {self.title}: {self.cost} || loc: {self.location}; date: {self.date} || wyr: {self.is_wyroznione} | {self.url}]'


async def check(url: str) -> list[Lot]:
    print(f"CHECKING [{url}]")
    page = await open_page(url)
    try:
        items = page.locator('div[data-cy=l-card]')
        lots = []
        print(f"{await items.count()} items found")
        for i in await items.all():
            try:
                lot = await Lot.create(i)
                lots.append(lot)
                print(lot)
            except Exception:
                traceback.print_exc()
                print("Unable to parse lot")
        return lots
    finally:
        try:
            await page.close()
        except Exception:
            pass


async def notify(lot: Lot, category: str = 'default') -> None:
    for sub in database.get_subscribers():
        try:
            await bot.send_message(sub, f'''
New advertisement in {category}

<b>{lot.title}</b>
Cost: {lot.cost}
Wyroznione: {lot.is_wyroznione}
Location: {lot.location}
Date: {lot.date}
link: <a href="{lot.url}">[CLICK]</a>

<blockquote expandable>
{await lot.description()}
'''[:1980] + '...\n</blockquote>')
        except:
            traceback.print_exc()
            print(f'Unable to notify {sub}')
    ...


async def filter_url(lot: Lot, cfg: UrlConfig) -> bool:
    if not cfg.filters: return True
    for f in cfg.filters:
        if f.lower() in lot.title.lower() or f.lower() in (await lot.description()).lower():
            return True
    return False


async def main():
    database.connect()
    await bot.start()
    async with async_playwright() as pw:
        global BROWSER
        BROWSER = await pw.chromium.launch()
        while True:
            for k, v in URL_LIST.items():
                try:
                    lots = await check(v.url)
                except:
                    print("Unable to check lots!")
                    lots = []
                for lot in lots:
                    if not database.check(lot.id, time_utils.parse_polish_datetime(lot.date)):
                        database.add(lot.id, time_utils.parse_polish_datetime(lot.date))
                        if await filter_url(lot, v):
                            await notify(lot, k)
                        else:
                            print(f"Lot: {lot.id} | {lot.title} doesnt pass!")
                _next = 30 + randint(-5, 5)
                print(f"NEXT check in {_next}s")
                await asyncio.sleep(_next)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        traceback.print_exc()
        s = traceback.format_exc()
        if len(s) % 1980 > 0:
            asyncio.run(bot.send_text_as_file(config.ADMIN, s, 'Bot error'))
        else:
            asyncio.run(bot.send_message(config.ADMIN, f'<blockquote expandable>{s}</blockquote>'))