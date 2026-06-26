# LangChain Training Guide

A comprehensive guide to building AI applications with LangChain and Anthropic's Claude API.

## 📚 What is LangChain?

LangChain is a framework for developing applications powered by language models. It enables:
- **Prompt Management**: Templates for efficient prompt engineering
- **Chains**: Sequences of operations (LLM calls, text processing, etc.)
- **Agents**: LLMs that can use tools (web search, calculators, APIs)
- **Memory**: Conversational context management
- **RAG**: Retrieval-Augmented Generation for knowledge-grounded responses
- **Integrations**: Support for multiple LLMs and vector stores

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup .env file
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY
```

### 2. Run Examples

```bash
# Basic LLM integration
python 01_basic_llm_integration.py

# Prompt templates
python 02_prompt_templates.py

# Chains
python 03_chains.py

# RAG pipeline
python 04_retrieval_rag.py

# Conversational memory
python 05_memory_conversation.py

# Agents with tools
python 06_agents_tools.py

# Document processing
python 07_document_processing.py
```

## 📖 Training Modules

### Module 1: Basic LLM Integration (01_basic_llm_integration.py)

**Concepts:**
- Initializing ChatAnthropic
- API configuration (model, temperature, max_tokens)
- Simple LLM invocation

**Key Parameters:**
```python
llm = ChatAnthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    model="claude-3-5-haiku-20241022",  # Model ID
    temperature=1.0,                     # Creativity (0=deterministic, 1=random)
    max_tokens=4096,                     # Response length
    top_k=None,                          # Top-K sampling (None = disabled)
    top_p=None,                          # Nucleus sampling (None = disabled)
    timeout=None,                        # Request timeout
    max_retries=2,                       # Retry failed requests
    stop=None,                           # Stop sequences
    streaming=False,                     # Stream response
    thinking=None,                       # Extended thinking config
    base_url="https://api.anthropic.com", # API endpoint
)
```

**Learning Outcomes:**
✓ Configure Claude for different use cases
✓ Understand LLM parameters
✓ Handle API responses

---

### Module 2: Prompt Templates (02_prompt_templates.py)

**Concepts:**
- PromptTemplate for string templates
- ChatPromptTemplate for multi-turn conversations
- Message roles (system, human, assistant)

**Examples:**

```python
# Simple template
prompt = PromptTemplate(
    input_variables=["topic"],
    template="Explain {topic} in simple terms."
)

# Chat template
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {specialty} expert."),
    ("human", "Tell me about {topic}")
])
```

**Learning Outcomes:**
✓ Reusable prompt templates
✓ Multi-turn conversations
✓ Message management

---

### Module 3: Chains (03_chains.py)

**Concepts:**
- Sequential processing with `|` operator
- Composing prompts, LLMs, and output parsers
- Running chains with `.invoke()`

**Examples:**

```python
# Simple chain
chain = prompt | llm | StrOutputParser()
result = chain.invoke({"topic": "AI"})

# Sequential chains
chain1 = prompt1 | llm | StrOutputParser()
chain2 = prompt2 | llm | StrOutputParser()

facts = chain1.invoke({"topic": "Python"})
quiz = chain2.invoke({"facts": facts})
```

**Learning Outcomes:**
✓ Compose LLM operations
✓ Chain multiple steps
✓ Build workflows

---

### Module 4: Retrieval-Augmented Generation (04_retrieval_rag.py)

**Concepts:**
- Loading documents (Wikipedia, PDFs, web)
- Text splitting and chunking
- Creating embeddings
- Vector store (ChromaDB)
- Retrieval and LLM augmentation

**RAG Pipeline:**

```
1. Load Documents
   ↓
2. Split into Chunks
   ↓
3. Create Embeddings (HuggingFace)
   ↓
4. Store in Vector DB (Chroma)
   ↓
5. Create Retriever
   ↓
6. Build Chain (Prompt + Retriever + LLM)
   ↓
7. Query and Get Augmented Response
```

**Learning Outcomes:**
✓ Knowledge-grounded responses
✓ Reduce hallucinations
✓ Use external knowledge bases

---

### Module 5: Memory & Conversation (05_memory_conversation.py)

**Concepts:**
- ConversationBufferMemory: Stores all messages
- ConversationSummaryMemory: Summarizes old messages
- Multi-turn conversations
- Context management

**Examples:**

```python
# Buffer memory
memory = ConversationBufferMemory(return_messages=True)
memory.save_context(
    {"input": "What's your name?"},
    {"output": "I'm Claude"}
)

# Retrieve history
history = memory.load_memory_variables({})
```

**Learning Outcomes:**
✓ Maintain conversation context
✓ Long-term memory management
✓ Multi-turn interactions

---

### Module 6: Agents & Tools (06_agents_tools.py)

**Concepts:**
- Defining tools (functions the agent can call)
- Tool calling agents
- AgentExecutor for running agents
- Using DuckDuckGo and Wikipedia as tools

**Agents:**

```python
tools = [search_tool, wiki_tool, calculator_tool]

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)

result = executor.invoke({"input": "Search for..."})
```

**Learning Outcomes:**
✓ Agentic AI systems
✓ Tool selection and calling
✓ Autonomous reasoning

---

### Module 7: Document Processing (07_document_processing.py)

**Concepts:**
- Document loaders (PDF, Web)
- Text splitting strategies
- Document summarization
- Information extraction

**Text Splitting:**

```python
# Character-based
splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20)

# Recursive (hierarchical)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    separators=["\n\n", "\n", " ", ""]
)
```

**Learning Outcomes:**
✓ Handle various document formats
✓ Optimize chunking strategies
✓ Extract key information

---

## 🎯 Key Concepts Explained

### Chains (| operator)

```python
# Sequential execution
chain = step1 | step2 | step3

# Equivalent to
chain = step1.pipe(step2).pipe(step3)

# Execution
result = chain.invoke(input_data)
```

### Output Parsers

```python
StrOutputParser()           # String output
JsonOutputParser()          # JSON structured output
PydanticOutputParser()      # Pydantic model validation
CommaSeparatedListOutputParser()  # CSV list
```

### Retrievers

```python
# Create retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Use in chain
chain = {"context": retriever, "question": lambda x: x}
```

### Memory Types

```python
ConversationBufferMemory()        # All messages (simple)
ConversationSummaryMemory()       # Summarized history (efficient)
ConversationKGMemory()            # Knowledge graph
ConversationEntityMemory()        # Entity tracking
```

---

## 📊 Architecture Diagram

```
┌─────────────────┐
│  User Input     │
└────────┬────────┘
         │
         v
┌─────────────────┐
│   Prompt Tmpl   │  (Format input)
└────────┬────────┘
         │
         v
┌─────────────────┐
│   Retriever     │  (Get context from vector DB)
└────────┬────────┘
         │
         v
┌─────────────────┐
│   LLM Chain     │  (Claude LLM)
└────────┬────────┘
         │
         v
┌─────────────────┐
│ Output Parser   │  (Format response)
└────────┬────────┘
         │
         v
┌─────────────────┐
│  Final Result   │
└─────────────────┘
```

---

## 🛠️ Common Patterns

### Pattern 1: Basic Query

```python
prompt = ChatPromptTemplate.from_template("Question: {query}")
chain = prompt | llm | StrOutputParser()
result = chain.invoke({"query": "What is AI?"})
```

### Pattern 2: RAG Query

```python
chain = (
    {"context": retriever, "query": lambda x: x}
    | prompt
    | llm
    | StrOutputParser()
)
result = chain.invoke("What about machine learning?")
```

### Pattern 3: Multi-step Workflow

```python
chain1 = prompt1 | llm | output_parser1
chain2 = prompt2 | llm | output_parser2

step1_result = chain1.invoke(input_data)
step2_result = chain2.invoke(step1_result)
```

### Pattern 4: Conditional Logic

```python
from langchain_core.runnables import RunnableBranch

branches = RunnableBranch(
    (lambda x: "AI" in x, chain_ai),
    (lambda x: "ML" in x, chain_ml),
    chain_default
)

result = branches.invoke(query)
```

---

## 🔐 Security Best Practices

✓ Use `.env` for all secrets
✓ Never hard-code API keys
✓ Use `python-dotenv` for configuration
✓ Validate user inputs
✓ Handle errors gracefully
✓ Set appropriate timeouts
✓ Monitor API usage

---

## 📦 Dependencies Explained

| Package | Purpose |
|---------|---------|
| langchain | Core framework |
| langchain-core | Base classes |
| langchain-community | Integrations |
| langchain-anthropic | Claude integration |
| anthropic | Anthropic SDK |
| chromadb | Vector store |
| sentence-transformers | Embeddings |
| duckduckgo-search | Web search |
| wikipedia | Wikipedia loader |
| beautifulsoup4 | HTML parsing |
| pydantic | Data validation |

---

## 🚨 Troubleshooting

### Issue: ImportError for langchain modules

**Solution:**
```bash
pip install --upgrade langchain langchain-core langchain-anthropic
```

### Issue: API Key not found

**Solution:**
1. Create `.env` file
2. Add `ANTHROPIC_API_KEY=your_key`
3. Ensure `.env` is in same directory as script

### Issue: Out of memory with large documents

**Solution:**
```python
# Use smaller chunks
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
```

### Issue: Slow retrieval

**Solution:**
```python
# Use semantic compression
compressor = LLMListCompressor.from_llm_and_prompt(llm, prompt)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=retriever
)
```

---

## 🎓 Learning Path

1. **Beginner** (1 hour)
   - Run Module 1 (Basic LLM)
   - Run Module 2 (Prompts)
   - Run Module 3 (Chains)

2. **Intermediate** (2 hours)
   - Run Module 4 (RAG)
   - Run Module 5 (Memory)
   - Understand components

3. **Advanced** (3+ hours)
   - Run Module 6 (Agents)
   - Run Module 7 (Documents)
   - Build custom applications

---

## 📚 Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Anthropic Claude API](https://console.anthropic.com/)
- [LangChain GitHub](https://github.com/langchain-ai/langchain)
- [RAG Concepts](https://arxiv.org/abs/2005.11401)

---

## ✅ Checklist

- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] `.env` file configured with API key
- [ ] Module 1 runs successfully
- [ ] Module 2 runs successfully
- [ ] Module 3 runs successfully
- [ ] Module 4 runs successfully
- [ ] Module 5 runs successfully
- [ ] Module 6 runs successfully
- [ ] Module 7 runs successfully
- [ ] Can build custom chains
- [ ] Understand RAG pipeline
- [ ] Ready for production use

---

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Review module documentation
3. Check LangChain docs
4. Review error messages carefully

---

**Happy Learning! 🚀**
