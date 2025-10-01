import asyncio
import pandas as pd
from playwright.async_api import async_playwright

async def search_and_scrape_internships(profile: str, location: str = None, last_days: int = None):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state="auth.json")
        page = await context.new_page()

        base_url = "https://internshala.com/internships"
        if location:
            url = f"{base_url}/location-{location}/keywords-{profile}"
        else:
            url = f"{base_url}/keywords-{profile}"

        await page.goto(url, wait_until="domcontentloaded")

        if last_days:
            await page.locator('//div[@class="filter_header" and contains(text(), "Posted On")]').click()
            await page.locator(f'//label[contains(text(), "Last {last_days} days")]').click()
            await page.get_by_role("button", name="Apply").click()
            await page.wait_for_load_state('domcontentloaded')

        internship_divs = await page.locator(".internship_meta").all()

        results = []
        for div in internship_divs[:10]: 
            title_element = div.locator(".internship_job_title .view_detail_button")
            company_element = div.locator(".company_and_premium_tag .company_name")
            stipend_element = div.locator(".stipend")

            title = await title_element.inner_text() if await title_element.count() > 0 else "N/A"
            company = await company_element.inner_text() if await company_element.count() > 0 else "N/A"
            stipend = await stipend_element.inner_text() if await stipend_element.count() > 0 else "N/A"

            results.append({
                "Title": title.strip(),
                "Company": company.strip(),
                "Stipend": stipend.strip()
            })

        await browser.close()

        if not results:
            return "No internships found with the specified criteria."

        df = pd.DataFrame(results)
        output_path = "internship_results.csv"
        df.to_csv(output_path, index=False)

        return f"Found {len(results)} internships. Details saved to {output_path}."