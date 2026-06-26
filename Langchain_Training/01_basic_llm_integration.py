from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os

load_dotenv(override=True)

llm = ChatAnthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    model="claude-3-5-haiku-20241022",
    temperature=1.0,
    max_tokens=4096,
    top_k=None,
    top_p=None,
    timeout=None,
    max_retries=2,
    stop=None,
    streaming=False,
    thinking=None,
    base_url="https://api.anthropic.com",
)

response = llm.invoke("What is Agentic AI?")
print("=" * 70)
print("Response from Claude:")
print("=" * 70)
print(response.content)
print("=" * 70)
