import asyncio
import sqlite3
from playwright.async_api import async_playwright
from urllib.parse import urljoin

async def search_and_scrape_internships(profile: str, location: str = None, last_days: int = None):
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
                pass

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
        return f"Scraped and saved {scraped_count} new internships."

async def download_and_search_chats(keyword: str = None):
    print(f"Starting chat scrape. Searching for keyword: {keyword}")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state="auth.json")
        page = await context.new_page()

        base_url = "https://internshala.com/"
        await page.goto(urljoin(base_url, "chat"), wait_until="domcontentloaded")
        
        conversation_links = await page.locator("a.chat_element").all()
        if not conversation_links:
            await browser.close()
            return "No conversations found on the main chat page."
            
        urls_to_visit = [urljoin(base_url, await link.get_attribute("href")) for link in conversation_links]
        print(f"Found {len(urls_to_visit)} conversations. Visiting each one...")
        
        all_messages = []
        for url in urls_to_visit:
            await page.goto(url, wait_until="domcontentloaded")
            
            try:
                sender_name = await page.locator("span.name").inner_text(timeout=5000)
            except Exception:
                continue
            
            message_containers = await page.locator(".message_history_element").all()

            for container in message_containers:
                msg_element = container.locator("pre.message_receiver")
                
                if await msg_element.count() > 0:
                    msg_text = await msg_element.inner_text()
                    
                    time_element = container.locator(".time")
                    timestamp = await time_element.inner_text() if await time_element.count() > 0 else ""
                    
                    if timestamp and msg_text.endswith(timestamp):
                        msg_text = msg_text[:-len(timestamp)].strip()

                    message_data = {"sender": sender_name, "content": msg_text, "link": url, "timestamp": timestamp}
                    
                    if keyword:
                        if keyword.lower() in msg_text.lower():
                            all_messages.append(message_data)
                    else:
                        all_messages.append(message_data)
        
        await browser.close()
        
        if not all_messages:
            return f"Search complete. No messages found containing the keyword: '{keyword}'"
            
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM messages")
        
        for msg in all_messages:
            cursor.execute("INSERT INTO messages (sender, content, link, timestamp) VALUES (?, ?, ?, ?)", 
                           (msg['sender'], msg['content'], msg['link'], msg['timestamp']))
        
        conn.commit()
        conn.close()
        
        return f"Found and saved {len(all_messages)} matching messages."
