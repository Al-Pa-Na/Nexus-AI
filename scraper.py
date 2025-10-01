import asyncio
import sqlite3
from playwright.async_api import async_playwright
from urllib.parse import urljoin

async def search_and_scrape_internships(profile: str, location: str = None, last_days: int = None):
    """
    Searches for internships on Internshala, scrapes the results, and saves them to a database.

    Args:
        profile: The job profile or keyword to search for.
        location: The city or location for the internship.
        last_days: Filter internships posted within the last number of days.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state="auth.json")
        page = await context.new_page()

        base_url = "https://internshala.com/"
        search_url = urljoin(base_url, "internships")
        
        if location:
            url = f"{search_url}/location-{location}/keywords-{profile}"
        else:
            url = f"{search_url}/keywords-{profile}"

        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            await browser.close()
            return f"Error: Failed to load the page. {e}"

        if last_days:
            try:
                await page.locator('//div[@class="filter_header" and contains(text(), "Posted On")]').click()
                await page.locator(f'//label[contains(text(), "Last {last_days} days")]').click()
                await page.get_by_role("button", name="Apply").click()
                await page.wait_for_load_state('domcontentloaded')
            except Exception:
                print("Could not apply date filter, proceeding without it.")

        internship_divs = await page.locator(".individual_internship").all()

        if not internship_divs:
            await browser.close()
            return "No internship containers found on the page."

        scraped_count = 0
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        for div in internship_divs:
            title_link_element = div.locator("a.job-title-href")
            company_element = div.locator(".company-name")
            # This is the updated, correct selector for the stipend
            stipend_element = div.locator(".stipend")

            title = await title_link_element.inner_text() if await title_link_element.count() > 0 else "N/A"
            if title == "N/A":
                continue

            company_raw = await company_element.inner_text() if await company_element.count() > 0 else "N/A"
            stipend = await stipend_element.inner_text() if await stipend_element.count() > 0 else "N/A"
            company = company_raw.split('\n')[0].strip()
            link_href = await title_link_element.get_attribute("href") if await title_link_element.count() > 0 else "#"
            link = urljoin(base_url, link_href)

            try:
                cursor.execute(
                    "INSERT OR IGNORE INTO internships (title, company, stipend, link) VALUES (?, ?, ?, ?)",
                    (title.strip(), company, stipend.strip(), link)
                )
                if cursor.rowcount > 0:
                    scraped_count += 1
            except sqlite3.IntegrityError:
                pass

        await browser.close()
        conn.commit()
        conn.close()
        
        print(f"Scraped and saved {scraped_count} new internships to the database.")
        return f"Scraped and saved {scraped_count} new internships."