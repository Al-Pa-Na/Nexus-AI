import os
import json
import asyncio
from openai import OpenAI
from dotenv import load_dotenv
import scraper 
import tools

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def run_conversation(user_prompt):
    messages = [{"role": "user", "content": user_prompt}]
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools.tools,
        tool_choice="auto",
    )
    
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        available_functions = {
            "search_and_scrape_internships": scraper.search_and_scrape_internships,
        }
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"🤖 AI is calling function '{function_name}' with arguments: {function_args}")
            
            function_response = await function_to_call(**function_args)
            print(f"\n✅ Result: {function_response}")

async def main():
    print("🚀 Welcome to the Internshala AI Automator!")
    print("Type your command, or 'exit' to quit.")
    
    while True:
        user_input = input("> ")
        if user_input.lower() == 'exit':
            break
        await run_conversation(user_input)

if __name__ == "__main__":
    asyncio.run(main())