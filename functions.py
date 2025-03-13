import asyncio
from agents import Agent, Runner, function_tool

@function_tool
def get_weather(city:str)->str:
    return f"The weather in {city} is very very cold."

agent = Agent(
    name="weather_agent",
    instructions="You are very helpful agent",
    tools=[get_weather]
)

async def main():
    result = await Runner.run(agent,input="What is the weather in Bahrain?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())