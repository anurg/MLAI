from agent import Agent, Runner
import asyncio

spanish_agent=Agent(
    name="spanish_agent",
    instructions="You only speak in spanish"
)
english_agent=Agent(
    name="english_agent",
    instructions="You only speak in english."
)
triage_agent=Agent(
    name="triage_agent",
    instructions="Hand off the control to appropriate agent based on the language of request",
    handoffs=[spanish_agent,english_agent]
)

async def main():
    # result=await Runner.run(triage_agent,input="Hola, ¿cómo estás?")
    result = await Runner.run(triage_agent,input="What is the capital of India")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
