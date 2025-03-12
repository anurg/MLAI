from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are very funny Assistant")

result = Runner.run_sync(agent, "Write a funny joke about OpenAI and Sam Altman")
print(result.final_output)