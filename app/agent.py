import os
import asyncio
import sqlite3
import google.generativeai as genai
from dotenv import load_dotenv
import app.scraper as scraper
import app.tools as tools

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found. Please check your .env file.")
genai.configure(api_key=api_key)


def format_internships_as_html(results):
    if not results:
        return "No internship results found in the database."
    
    table_html = "<table><thead><tr><th>Internship</th><th>Company</th><th>Stipend</th></tr></thead><tbody>"
    for row in results:
        _id, title, company, stipend, link, _scraped_at = row
        table_html += f'<tr><td><a href="{link}" target="_blank">{title}</a></td><td>{company}</td><td>{stipend}</td></tr>'
    table_html += "</tbody></table>"
    return table_html


def format_chats_as_html(results):
    if not results:
        return "No chat messages found in the database."
    
    html = "<ul>"
    for row in results:
        _id, sender, content, timestamp, _link, _scraped_at = row
        html += f"<li><strong>{sender}:</strong> {content} <span style='color: #888; font-size: 0.8em;'>({timestamp})</span></li>"
    html += "</ul>"
    return html


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
        function_name = function_call.name
        function_args = dict(function_call.args)
        
        print(f"🤖 AI is calling function '{function_name}' with arguments: {function_args}")

        if function_name == "search_and_scrape_internships":
            await scraper.search_and_scrape_internships(**function_args)
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM internships ORDER BY scraped_at DESC LIMIT 10")
            db_results = cursor.fetchall()
            conn.close()
            return format_internships_as_html(db_results)
        
        elif function_name == "download_and_search_chats":
            await scraper.download_and_search_chats(**function_args)
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM messages ORDER BY id DESC")
            db_results = cursor.fetchall()
            conn.close()
            return format_chats_as_html(db_results)
        
        else:
            return f"Error: AI requested an unknown function '{function_name}'."

    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        print(error_message)
        return error_message