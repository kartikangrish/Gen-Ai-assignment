from langchain.document_loaders import PyPDFLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
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
print("Document Processing with LangChain")
print("=" * 70)

print("\n1. Loading from Web...")
try:
    loader = WebBaseLoader("https://en.wikipedia.org/wiki/Artificial_intelligence")
    docs = loader.load()
    print(f"✓ Loaded {len(docs)} web documents")
    print(f"  First doc length: {len(docs[0].page_content)} characters")
except Exception as e:
    print(f"Note: Web loader requires internet: {str(e)[:50]}")
    print("Creating sample document for demonstration...")

    from langchain.schema import Document

    sample_content = """
    Artificial Intelligence (AI) is the simulation of human intelligence processes
    by computer systems. These processes include learning, reasoning, and
    self-correction. AI has applications in healthcare, finance, and many other
    industries. Machine Learning is a subset of AI that enables systems to learn
    from data. Deep Learning uses neural networks with multiple layers.
    """

    docs = [Document(page_content=sample_content)]

print("\n2. Text Splitting Strategies...")

print("\n  a) Character-based Splitting:")
splitter_char = CharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20,
    separator=" "
)

chunks_char = splitter_char.split_documents(docs)
print(f"  ✓ Created {len(chunks_char)} chunks")
print(f"    First chunk: {chunks_char[0].page_content[:100]}...")

print("\n  b) Recursive Character Splitting:")
splitter_recursive = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50,
    separators=["\n\n", "\n", " ", ""]
)

chunks_recursive = splitter_recursive.split_documents(docs)
print(f"  ✓ Created {len(chunks_recursive)} chunks")
print(f"    First chunk: {chunks_recursive[0].page_content[:100]}...")

print("\n3. Document Summarization...")

prompt_summary = ChatPromptTemplate.from_template("""
Summarize the following text in 2-3 sentences:

Text:
{text}

Summary:
""")

chain_summary = prompt_summary | llm | StrOutputParser()

summary = chain_summary.invoke({"text": docs[0].page_content})
print(f"\nSummary:\n{summary}")

print("\n4. Extracting Key Information...")

prompt_extract = ChatPromptTemplate.from_template("""
Extract the main topics from this text. List them as bullet points.

Text:
{text}

Topics:
""")

chain_extract = prompt_extract | llm | StrOutputParser()

topics = chain_extract.invoke({"text": docs[0].page_content})
print(f"\nExtracted Topics:\n{topics}")

print("\n5. Processing Multiple Documents...")

print(f"Total documents: {len(docs)}")
print(f"Total chunks: {len(chunks_recursive)}")

for i, chunk in enumerate(chunks_recursive[:2]):
    print(f"\nChunk {i+1}:")
    print(f"  Content: {chunk.page_content[:100]}...")
    print(f"  Metadata: {chunk.metadata}")
