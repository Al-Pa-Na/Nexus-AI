import os
import asyncio
import sqlite3
import google.generativeai as genai
from dotenv import load_dotenv
import scraper
import tools

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found. Please check your .env file.")
genai.configure(api_key=api_key)


def format_results_as_html(results):
    if not results:
        return "No results found in the database."
    
    table_html = "<table><thead><tr><th>Internship</th><th>Company</th><th>Stipend</th></tr></thead><tbody>"
    for row in results:
        _id, title, company, stipend, link, _scraped_at = row
        table_html += f'<tr><td><a href="{link}" target="_blank">{title}</a></td><td>{company}</td><td>{stipend}</td></tr>'
    table_html += "</tbody></table>"
    return table_html


async def run_conversation(user_prompt):
    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            tools=tools.tools
        )
        
        chat = model.start_chat()
        response = chat.send_message(user_prompt)
        part = response.candidates[0].content.parts[0]

        if not hasattr(part, 'function_call'):
            return "I'm sorry, I couldn't determine an action from your command."

        function_call = part.function_call
        function_args = dict(function_call.args)
        
        print(f"🤖 AI is calling function '{function_call.name}' with arguments: {function_args}")

        await scraper.search_and_scrape_internships(**function_args)
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM internships ORDER BY scraped_at DESC LIMIT 10")
        db_results = cursor.fetchall()
        conn.close()
        
        return format_results_as_html(db_results)

    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        print(error_message)
        return error_message