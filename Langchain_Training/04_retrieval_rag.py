from langchain_anthropic import ChatAnthropic
from langchain_community.document_loaders import WikipediaLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
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
print("LangChain RAG Pipeline")
print("=" * 70)

print("\n1. Loading Documents...")
loader = WikipediaLoader(query="Machine Learning")
docs = loader.load()
print(f"✓ Loaded {len(docs)} documents")

print("\n2. Splitting Documents...")
text_splitter = CharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)
splits = text_splitter.split_documents(docs)
print(f"✓ Created {len(splits)} text chunks")

print("\n3. Creating Embeddings...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
print("✓ Embeddings model loaded")

print("\n4. Creating Vector Store...")
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    collection_name="ml_knowledge"
)
print("✓ Vector store created with Chroma")

print("\n5. Creating Retriever...")
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
print("✓ Retriever ready")

print("\n6. Building RAG Chain...")

prompt = ChatPromptTemplate.from_template("""
You are a helpful AI assistant about Machine Learning.
Use the following context to answer the question.

Context:
{context}

Question: {question}

Answer based on the context provided:
""")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

chain = (
    {
        "context": retriever | (lambda docs: format_docs(docs)),
        "question": lambda x: x["question"]
    }
    | prompt
    | llm
    | StrOutputParser()
)

print("✓ Chain created")

print("\n7. Testing RAG Pipeline...")
question = "What are the key applications of machine learning?"

result = chain.invoke({"question": question})

print(f"\nQuestion: {question}")
print("\nAnswer:")
print(result)
