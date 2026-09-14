import asyncio
import requests
from playwright.async_api import async_playwright

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbw9kL7nhR4NlAk3W2HZhc9A3ff5XovczbC9mSKdMXqVdtBCPdtyU87JKmrvx50Zp0hK/exec"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
        page = await browser.new_page()
        print("mse.mn сайтаас өгөгдөл татаж байна...")

        await page.goto("https://www.mse.mn/todays-trade", wait_until="networkidle")
        await page.wait_for_timeout(3000)

        rows_data = []
        rows = await page.query_selector_all("table tbody tr")
        for row in rows:
            cols = []
            col_elements = await row.query_selector_all("td")
            for col in col_elements:
                text = await col.inner_text()
                cols.append(text.strip())
            if cols:
                rows_data.append(cols)

        await browser.close()

        if rows_data:
            print(f"{len(rows_data)} мөр өгөгдөл олоод Google Sheets рүү илгээж байна...")
            res = requests.post(WEB_APP_URL, json=rows_data)
            print("Үр дүн:", res.text)
        else:
            print("Дата олдсонгүй.")

if __name__ == "__main__":
    asyncio.run(main())
