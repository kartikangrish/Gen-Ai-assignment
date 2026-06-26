from langchain_anthropic import ChatAnthropic
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
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
print("1. Conversation Buffer Memory")
print("=" * 70)

memory = ConversationBufferMemory(return_messages=True)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])

chain = prompt | llm | StrOutputParser()

conversations = [
    "Hi, my name is Alice",
    "What's 2 + 2?",
    "What's my name?",
    "Tell me about AI",
    "Do you remember my name?",
]

print("\nConversation:")
for user_input in conversations:
    print(f"\nUser: {user_input}")

    chat_history = memory.load_memory_variables({})["history"]

    response = chain.invoke({
        "chat_history": chat_history,
        "input": user_input
    })

    print(f"AI: {response[:200]}...")

    memory.save_context(
        {"input": user_input},
        {"output": response}
    )

print("\n" + "=" * 70)
print("2. Conversation Summary Memory")
print("=" * 70)

summary_memory = ConversationSummaryMemory(
    llm=llm,
    return_messages=True
)

print("\nStoring conversation with summary:")
for user_input in conversations[:3]:
    print(f"User: {user_input}")

    summary_history = summary_memory.load_memory_variables({})["history"]

    response = chain.invoke({
        "chat_history": summary_history,
        "input": user_input
    })

    print(f"AI: {response[:150]}...")

    summary_memory.save_context(
        {"input": user_input},
        {"output": response}
    )

print("\n" + "=" * 70)
print("3. Extracting Memory")
print("=" * 70)

print(f"\nBuffer Memory Variables:")
print(memory.load_memory_variables({}))

print(f"\nSummary Memory Variables:")
print(summary_memory.load_memory_variables({}))
