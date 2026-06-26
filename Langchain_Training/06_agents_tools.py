from langchain_anthropic import ChatAnthropic
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper, WikipediaAPIWrapper
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
import os

load_dotenv(override=True)

llm = ChatAnthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    model="claude-3-5-haiku-20241022",
    temperature=0.7,
    max_tokens=2048,
)

print("=" * 70)
print("LangChain Agents with Tools")
print("=" * 70)

print("\n1. Defining Tools...")

search_wrapper = DuckDuckGoSearchAPIWrapper()
search_tool = DuckDuckGoSearchRun(api_wrapper=search_wrapper)

wiki_wrapper = WikipediaAPIWrapper()
wiki_tool = WikipediaQueryRun(api_wrapper=wiki_wrapper)

tools = [search_tool, wiki_tool]

print(f"✓ Created {len(tools)} tools:")
for tool in tools:
    print(f"  - {tool.name}: {tool.description[:60]}...")

print("\n2. Creating Agent Prompt...")

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful AI assistant that can search the web and
     access Wikipedia. Use the available tools to answer questions accurately.
     Be helpful and thorough in your responses."""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

print("✓ Prompt template created")

print("\n3. Creating Agent...")

agent = create_tool_calling_agent(llm, tools, prompt)

executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=3,
)

print("✓ Agent executor ready")

print("\n4. Running Agent with Tool Use...")

queries = [
    "What is LangChain and when was it created?",
    "Tell me about Retrieval-Augmented Generation (RAG)",
]

for query in queries:
    print(f"\n{'='*70}")
    print(f"Query: {query}")
    print("=" * 70)

    try:
        result = executor.invoke({
            "input": query,
            "chat_history": [],
            "agent_scratchpad": "",
        })

        print(f"\nFinal Answer: {result.get('output', 'No response')[:300]}...")

    except Exception as e:
        print(f"Error: {str(e)[:200]}")
        print(f"\nNote: Tool calling may require API setup")
