# GenAI Flask-Chroma Knowledge Assistant

A Flask-based web application that implements Retrieval-Augmented Generation (RAG) using ChromaDB vector database and LLM API integration.

## Features

✅ **RAG Architecture** - Retrieves relevant context from ChromaDB before generating LLM responses  
✅ **Vector Embeddings** - Uses SentenceTransformer to convert questions into semantic vectors  
✅ **ChromaDB Integration** - Stores and searches 10 curated GenAI knowledge chunks  
✅ **LLM API** - Integrates with Anthropic Claude API for answer generation  
✅ **Web UI** - Simple and intuitive Flask HTML interface  
✅ **Error Handling** - Handles 401, 404, 405 HTTP errors gracefully  
✅ **Security** - API keys stored in .env, not hard-coded  
✅ **Prompt Engineering** - Uses persona, context, task, and constraints  

## Project Structure

```
genai-flask-chroma-assistant/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (API keys)
├── README.md             # This file
├── templates/
│   └── index.html        # Web UI form and display
├── static/
│   └── style.css         # Styling for the interface
└── chroma_db/            # Auto-created persistent vector database
```

## Setup Instructions

### 1. Create Project Folder
```bash
mkdir genai-flask-chroma-assistant
cd genai-flask-chroma-assistant
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure .env File
Edit `.env` with your credentials:
```
ANTHROPIC_API_KEY=your_actual_api_key
LLM_ENDPOINT=https://api.anthropic.com/v1/messages
LLM_MODEL=claude-3-5-sonnet-20241022
```

### 5. Run Flask App
```bash
python app.py
```

The app will start at `http://localhost:5000`

## How It Works

### End-to-End RAG Flow

1. **User submits question** → Flask receives it via POST request
2. **Generate embedding** → SentenceTransformer converts question to vector
3. **Search ChromaDB** → Vector similarity search finds top 3 relevant chunks
4. **Prepare prompt** → Adds persona, context, task, and constraints
5. **Call LLM API** → Sends prompt to Claude with retrieved context
6. **Display results** → Shows question, context, distances, and answer

### Example Output

**Question:** What is the role of embeddings in GenAI?

**Retrieved Context:**
- Embeddings are numerical vector representations that capture semantic meaning of text
- Semantic search compares meaning rather than exact words using embeddings
- Vector databases store embeddings and retrieve semantically relevant information

**Assistant Response:**
Embeddings help GenAI systems understand the meaning of text by converting words or sentences into numerical vectors. These vectors allow the application to compare meanings, retrieve relevant context from ChromaDB, and provide better responses through the LLM.

## Evaluation Criteria

| Area | Details |
|------|---------|
| **Flask UI** | Users can submit questions and view answers with retrieved context |
| **ChromaDB** | 10 knowledge chunks stored with topics and metadata |
| **Embeddings** | SentenceTransformer (all-MiniLM-L6-v2) generates query embeddings |
| **Retrieval** | Top 3 relevant documents retrieved using vector similarity |
| **LLM Integration** | Claude API called with proper headers, auth, and payload |
| **Security** | API key loaded from .env, not hard-coded |
| **Prompt Engineering** | Includes persona, context, task, and constraints |
| **Error Handling** | 401 (Auth), 404 (Endpoint), 405 (Method) errors handled |
| **RAG Readiness** | Context retrieved before generating answer |

## Knowledge Base

The application includes 10 curated knowledge chunks on:
- Embeddings and semantic meaning
- Semantic search techniques
- Vector databases (ChromaDB)
- RAG (Retrieval-Augmented Generation)
- Transformers and attention mechanisms
- Prompt engineering strategies
- SentenceTransformer framework
- ChromaDB database
- Large Language Models (LLMs)
- Generative AI (GenAI) concepts

## How ChromaDB Helps RAG

ChromaDB is a vector database optimized for:

1. **Semantic Storage** - Stores embeddings alongside original text and metadata
2. **Fast Retrieval** - Uses efficient similarity search to find relevant documents quickly
3. **Scalability** - Handles large document collections with persistent storage
4. **Metadata Filtering** - Can filter results by topic or other metadata
5. **Integration** - Works seamlessly with Python applications and SentenceTransformer

In RAG applications, ChromaDB acts as the knowledge base that provides context to the LLM. Instead of relying only on the LLM's training data, the system first retrieves relevant information from ChromaDB, ensuring more accurate and up-to-date responses.

## Error Handling

The application gracefully handles:
- **401 Unauthorized** - Invalid API key
- **404 Not Found** - Wrong endpoint URL
- **405 Method Not Allowed** - Incorrect HTTP method
- **503 Service Unavailable** - Network errors
- **504 Gateway Timeout** - Request timeout
- **500 Internal Server Error** - JSON parsing or unexpected errors

## Technologies Used

- **Flask** - Web framework
- **SentenceTransformer** - Embedding generation
- **ChromaDB** - Vector database
- **Requests** - HTTP client for LLM API
- **Python-dotenv** - Environment variable management
- **HTML/CSS/JavaScript** - Frontend interface

## Troubleshooting

**Issue: Port 5000 already in use**
```bash
# Use a different port
python -c "from app import app; app.run(port=5001)"
```

**Issue: API key not loading**
- Ensure .env file is in the same directory as app.py
- Check that ANTHROPIC_API_KEY value is set correctly
- Restart Flask app after updating .env

**Issue: ChromaDB not found**
- Delete `chroma_db` folder to reset the database
- Re-run app to reinitialize with default knowledge chunks

## Security Notes

⚠️ Never commit `.env` file to version control  
⚠️ Never share API keys in chat or documentation  
⚠️ Use environment variables for all secrets  
⚠️ Rotate API keys periodically  

## Future Enhancements

- Add user feedback system for answer quality
- Implement multiple vector databases
- Support different embedding models
- Add question history and persistence
- Implement streaming LLM responses
- Add admin interface to manage knowledge base
- Support for different LLM providers

## License

Educational Use Only - GenAI Foundations Training

## Support

For issues or questions about this assignment, refer to the GenAI Foundations training materials.
