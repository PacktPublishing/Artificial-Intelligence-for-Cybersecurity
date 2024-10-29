# Example from https://securemachinery.com/2023/03/25/langchain-example/
# The purpose is showing how to use the langchain and openAI api to create a AI workload
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
llm = OpenAI(temperature=0)
tools = load_tools(["serpapi", "llm-math"], llm=llm)
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
agent.run("how can one fine-tune a generative ai llm model ?")
