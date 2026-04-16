import asyncio
import json
import os
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False) 
        page = await browser.new_page()

        all_raw_jobs = {} 

        print("📡 Intercepting EVERYTHING from Algolia...")

        async def handle_response(response):
            if "algolia" in response.url and response.status == 200:
                try:
                    data = await response.json()
                    for result in data.get("results", []):
                        hits = result.get("hits", [])
                        for job in hits:
                            slug = job.get('slug')
                            if slug:
                                all_raw_jobs[slug] = {
                                    "title": job.get("name"),
                                    "company": job.get("organization", {}).get("name"),
                                    "location": job.get("office", {}).get("city"),
                                    "contract": job.get("contract_type"), # چک کردن نام دقیق قرارداد
                                    "link": f"https://www.welcometothejungle.com/fr/jobs/{slug}"
                                }
                except:
                    pass

        page.on("response", handle_response)

        target_url = "https://www.welcometothejungle.com/fr/jobs?query=developer&aroundQuery=Paris%2C%20France"
        await page.goto(target_url, wait_until="networkidle")
        
        print("🖱 Scrolling...")
        await page.mouse.wheel(0, 2000)
        await asyncio.sleep(5)

        final_list = list(all_raw_jobs.values())

        if final_list:
            base_path = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(base_path, 'jobs_data.json')
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(final_list, f, ensure_ascii=False, indent=4)
            print(f"✅ Success! Found {len(final_list)} raw jobs. Check the JSON file now.")
        else:
            print("❌ Still zero. This means Algolia calls are not being intercepted.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
