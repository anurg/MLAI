from agent import Agent, Runner
import asyncio

spanish_agent=Agent(
    name="Spanish Agent",
    instructions="You only speak in spanish"
)
english_agent=Agent(
    name="English Agent",
    instructions="You only speak in english."
)

triage_agent=Agent(
    name="Triage Agent",
    instructions="Hand off to the appropriate agent based on the language of request",
    handoffs=[spanish_agent,english_agent]
    )

async def main():
    # result = await Runner.run(triage_agent,input="Hola, ¿cómo estás?")
    result = await Runner.run(triage_agent,input="Hi, How are you?")

    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())


