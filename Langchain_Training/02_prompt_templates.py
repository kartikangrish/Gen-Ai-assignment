from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
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
print("1. Simple Prompt Template")
print("=" * 70)

prompt = PromptTemplate(
    input_variables=["topic"],
    template="Explain the concept of {topic} in simple terms for a beginner."
)

formatted_prompt = prompt.format(topic="Machine Learning")
response = llm.invoke(formatted_prompt)
print(f"Topic: Machine Learning")
print(f"Response: {response.content[:200]}...")

print("\n" + "=" * 70)
print("2. Chat Prompt Template")
print("=" * 70)

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant specialized in {specialty}."),
    ("human", "Tell me about {topic}")
])

messages = chat_prompt.format_messages(
    specialty="data science",
    topic="neural networks"
)

response = llm.invoke(messages)
print(f"Specialty: Data Science")
print(f"Topic: Neural Networks")
print(f"Response: {response.content[:200]}...")

print("\n" + "=" * 70)
print("3. Multi-turn Conversation")
print("=" * 70)

messages = [
    SystemMessage(content="You are a knowledgeable Python expert."),
    HumanMessage(content="What is a lambda function?"),
]

response = llm.invoke(messages)
print(f"Q: What is a lambda function?")
print(f"A: {response.content[:150]}...")

messages.append(response)
messages.append(HumanMessage(content="Can you provide an example?"))

response = llm.invoke(messages)
print(f"\nQ: Can you provide an example?")
print(f"A: {response.content[:150]}...")
