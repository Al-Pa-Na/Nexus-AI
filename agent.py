import os
import json
import asyncio
from openai import OpenAI, RateLimitError
from dotenv import load_dotenv
import scraper
import tools

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def run_conversation(user_prompt):
    messages = [{"role": "user", "content": user_prompt}]
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools.tools,
            tool_choice="auto",
        )
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if not tool_calls:
            return "I'm sorry, I couldn't determine an action from your command. Please try again."

        available_functions = {
            "search_and_scrape_internships": scraper.search_and_scrape_internships,
        }
        
        tool_call = tool_calls[0]
        function_name = tool_call.function.name
        function_to_call = available_functions[function_name]
        function_args = json.loads(tool_call.function.arguments)
        
        print(f"🤖 AI is calling function '{function_name}' with arguments: {function_args}")
        
        function_response = await function_to_call(**function_args)
        return f"✅ Result: {function_response}"

    except RateLimitError:
        error_message = "Error: Your OpenAI API quota has been exceeded. Please check your plan and billing details."
        print(error_message)
        return error_message
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        print(error_message)
        return error_message