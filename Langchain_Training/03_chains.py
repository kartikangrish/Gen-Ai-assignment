from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
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
print("1. Simple Chain: Prompt → LLM → Output")
print("=" * 70)

prompt = ChatPromptTemplate.from_template(
    "Write a short poem about {topic} in 4 lines."
)

chain = prompt | llm | StrOutputParser()

result = chain.invoke({"topic": "Artificial Intelligence"})
print(f"Topic: Artificial Intelligence")
print(f"Poem:\n{result}")

print("\n" + "=" * 70)
print("2. Sequential Chain: Multiple Prompts")
print("=" * 70)

prompt1 = ChatPromptTemplate.from_template(
    "Generate 3 interesting facts about {topic}."
)

chain1 = prompt1 | llm | StrOutputParser()

facts = chain1.invoke({"topic": "Python Programming"})
print(f"3 Facts about Python:\n{facts[:300]}...")

prompt2 = ChatPromptTemplate.from_template(
    "Create a quiz question based on this information:\n{facts}"
)

chain2 = prompt2 | llm | StrOutputParser()

quiz = chain2.invoke({"facts": facts})
print(f"\nQuiz Question:\n{quiz[:300]}...")

print("\n" + "=" * 70)
print("3. Chained Operations")
print("=" * 70)

prompt_analyze = ChatPromptTemplate.from_template(
    "Analyze the sentiment of: {text}"
)

prompt_expand = ChatPromptTemplate.from_template(
    "Expand on this analysis: {analysis}"
)

chain_analyze = prompt_analyze | llm | StrOutputParser()
chain_expand = prompt_expand | llm | StrOutputParser()

text = "I love working with AI, it's amazing and transformative!"

sentiment = chain_analyze.invoke({"text": text})
print(f"Text: {text}")
print(f"Sentiment Analysis:\n{sentiment[:200]}...\n")

expanded = chain_expand.invoke({"analysis": sentiment})
print(f"Expanded Analysis:\n{expanded[:200]}...")
