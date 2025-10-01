import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urljoin

async def search_and_scrape_internships(profile: str, location: str = None, last_days: int = None):
    """
    Searches for internships on Internshala, scrapes the results, and returns them as an HTML table.

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
            return "No internships found for the specified criteria on the page."

        results = []
        for div in internship_divs:
            # Using the new, correct selector you found
            title_link_element = div.locator("a.job-title-href")
            company_element = div.locator(".company-name")
            stipend_element = div.locator(".item_body")

            title = await title_link_element.inner_text() if await title_link_element.count() > 0 else "N/A"
            company_raw = await company_element.inner_text() if await company_element.count() > 0 else "N/A"
            stipend = await stipend_element.inner_text() if await stipend_element.count() > 0 else "N/A"
            
            company = company_raw.split('\n')[0].strip()
            
            link_href = await title_link_element.get_attribute("href") if await title_link_element.count() > 0 else "#"
            link = urljoin(base_url, link_href)

            if title != "N/A":
                results.append({
                    "Title": f'<a href="{link}" target="_blank">{title.strip()}</a>',
                    "Company": company,
                    "Stipend": stipend.strip()
                })

        await browser.close()
        
        if not results:
            return "Found internship containers, but could not extract valid data."

        table_html = "<table><thead><tr><th>Internship</th><th>Company</th><th>Stipend</th></tr></thead><tbody>"
        for r in results:
            table_html += f"<tr><td>{r['Title']}</td><td>{r['Company']}</td><td>{r['Stipend']}</td></tr>"
        table_html += "</tbody></table>"

        return table_html