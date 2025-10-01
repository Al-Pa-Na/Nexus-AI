import os
import asyncio
import google.generativeai as genai
from dotenv import load_dotenv
import scraper
import tools

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file. Please add it.")
genai.configure(api_key=api_key)

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
            return "I'm sorry, I couldn't determine an action. Please try a different command."

        function_call = part.function_call
        function_name = function_call.name
        
        available_functions = {
            "search_and_scrape_internships": scraper.search_and_scrape_internships,
        }
        
        if function_name not in available_functions:
            return f"Error: The AI tried to call an unknown function '{function_name}'."
        
        function_to_call = available_functions[function_name]
        function_args = dict(function_call.args)
        
        print(f"🤖 AI is calling function '{function_name}' with arguments: {function_args}")
        
        function_response = await function_to_call(**function_args)
        return function_response

    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        print(error_message)
        return error_message