import asyncio
from agent import run_conversation

async def main():
    print("🚀 Welcome to the Nexus AI CLI!")
    print("Type your command, or 'exit' to quit.")
    
    while True:
        user_input = input("> ")
        if user_input.lower() == 'exit':
            break
        result = await run_conversation(user_input)
        print(result)

if __name__ == "__main__":
    asyncio.run(main())