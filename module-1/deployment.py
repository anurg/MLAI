from langgraph_sdk import get_client
import asyncio
from langchain_core.messages import HumanMessage

URL = "http://127.0.0.1:2024"
client = get_client(url=URL)

async def get_assistants():
    assistants = await client.assistants.search()
    return assistants

async def create_thread():
    thread = await client.threads.create()
    return thread

async def stream_run(thread_id, input_data):
    async for chunk in client.runs.stream(
        thread_id,
        "agent",
        input=input_data,
        stream_mode="values",
    ):
        if chunk.data and chunk.event != "metadata":
            print(chunk.data['messages'][-1])

async def main():
    # Create thread
    thread = await create_thread()
    print(f"Thread created with ID: {thread['thread_id']}")
    
    # Define your input
    input_message = HumanMessage(content="Multiply 2 and 3 and give output")
    
    # Stream run with the new thread
    await stream_run(thread['thread_id'], input_message)
    
    # Optionally get assistants if needed
    # assistants = await get_assistants()
    # print(assistants)

if __name__ == "__main__":
    asyncio.run(main())