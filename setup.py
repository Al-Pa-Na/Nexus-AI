import asyncio
import os
from playwright.async_api import async_playwright

# We are pointing to a new folder that Playwright will create.
# This will be our small, dedicated profile for automation.
PROFILE_DIR = "./MyPlaywrightProfile" 

async def main():
    print("--- Script Starting: Creating a new, lightweight profile ---")

    try:
        async with async_playwright() as p:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=PROFILE_DIR, # Giving it the path to the new folder
                headless=False,
                channel="chrome"
            )
            page = context.pages[0] if context.pages else await context.new_page()
            
            print("\n✅ A new, clean Chrome window has opened.")
            print("➡️ Please log in to Internshala one time in this window.")
            print("This will save your session in our new, small profile.")
            
            await page.goto("https://internshala.com/login/student")
            
            print("\nOnce you are fully logged in, press Enter here in the terminal...")
            input() 
            
            await context.storage_state(path="auth.json")
            print("\n✅ Authentication state saved successfully!")
            await context.close()
            
    except Exception as e:
        print(f"\n--- AN ERROR OCCURRED ---\n{e}")

if __name__ == "__main__":
    asyncio.run(main())