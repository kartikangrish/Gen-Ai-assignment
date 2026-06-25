import os
import json
import requests
from flask import Flask, render_template, request, jsonify
from sentence_transformers import SentenceTransformer
import chromadb
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("ANTHROPIC_API_KEY")
LLM_ENDPOINT = os.getenv("LLM_ENDPOINT")
LLM_MODEL = os.getenv("LLM_MODEL")

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="genai_knowledge")

def initialize_knowledge_base():
    if collection.count() == 0:
        knowledge_chunks = [
            {
                "id": "1",
                "text": "Embeddings are numerical vector representations that capture semantic meaning of text. They convert words or sentences into fixed-size arrays of numbers.",
                "metadata": {"topic": "embeddings"}
            },
            {
                "id": "2",
                "text": "Semantic search compares meaning rather than exact words using embeddings. It allows finding similar content even if the exact wording is different.",
                "metadata": {"topic": "semantic_search"}
            },
            {
                "id": "3",
                "text": "Vector databases like ChromaDB store embeddings and retrieve semantically relevant information efficiently using similarity search.",
                "metadata": {"topic": "vector_databases"}
            },
            {
                "id": "4",
                "text": "RAG stands for Retrieval-Augmented Generation. It retrieves relevant context from a knowledge base first, then uses that context to generate better LLM responses.",
                "metadata": {"topic": "rag"}
            },
            {
                "id": "5",
                "text": "Transformers are neural network architectures that use self-attention mechanisms. They power modern LLMs like GPT and Claude.",
                "metadata": {"topic": "transformers"}
            },
            {
                "id": "6",
                "text": "Prompt engineering involves crafting effective prompts to guide LLMs. Key techniques include providing context, examples, and clear instructions.",
                "metadata": {"topic": "prompt_engineering"}
            },
            {
                "id": "7",
                "text": "SentenceTransformer is a framework for generating sentence embeddings. It provides pre-trained models that can be used to encode text into dense vectors.",
                "metadata": {"topic": "embeddings"}
            },
            {
                "id": "8",
                "text": "ChromaDB is an open-source vector database designed for storing and retrieving embeddings. It integrates seamlessly with Python applications.",
                "metadata": {"topic": "vector_databases"}
            },
            {
                "id": "9",
                "text": "Large Language Models (LLMs) are AI models trained on vast amounts of text data. They can generate human-like text, answer questions, and perform various NLP tasks.",
                "metadata": {"topic": "llms"}
            },
            {
                "id": "10",
                "text": "GenAI refers to generative AI systems that can create new content like text, images, or code. Foundation models like GPT and Claude are examples of GenAI.",
                "metadata": {"topic": "genai"}
            }
        ]

        for chunk in knowledge_chunks:
            embedding = embedding_model.encode(chunk["text"])
            collection.add(
                ids=[chunk["id"]],
                embeddings=[embedding.tolist()],
                documents=[chunk["text"]],
                metadatas=[chunk["metadata"]]
            )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def process_query():
    try:
        data = request.json
        user_question = data.get('question', '').strip()

        if not user_question:
            return jsonify({'error': 'Question cannot be empty'}), 400

        question_embedding = embedding_model.encode(user_question)

        results = collection.query(
            query_embeddings=[question_embedding.tolist()],
            n_results=3,
            include=["documents", "distances", "metadatas"]
        )

        retrieved_docs = results['documents'][0] if results['documents'] else []
        distances = results['distances'][0] if results['distances'] else []

        context = "\n".join([f"- {doc}" for doc in retrieved_docs])

        persona = "You are a friendly and knowledgeable GenAI education assistant."
        task = "Answer the user's question clearly and concisely, suitable for beginners."
        constraints = "Keep the response under 150 words. Use simple language."

        prompt = f"""
{persona}

Context from knowledge base:
{context}

Task: {task}

Constraints: {constraints}

User Question: {user_question}

Provide a helpful answer based on the context above.
"""

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": LLM_MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 300
        }

        response = requests.post(LLM_ENDPOINT, headers=headers, json=payload, timeout=30)

        if response.status_code == 401:
            return jsonify({'error': 'Authentication failed. Check your API key.'}), 401
        elif response.status_code == 404:
            return jsonify({'error': 'LLM endpoint not found. Check your endpoint URL.'}), 404
        elif response.status_code == 405:
            return jsonify({'error': 'Method not allowed. Check your endpoint configuration.'}), 405
        elif response.status_code != 200:
            return jsonify({'error': f'LLM API error: {response.status_code}'}), response.status_code

        response_data = response.json()
        assistant_response = response_data['content'][0]['text']

        return jsonify({
            'question': user_question,
            'retrieved_context': retrieved_docs,
            'distances': distances,
            'assistant_response': assistant_response
        }), 200

    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request to LLM API timed out'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Network error: {str(e)}'}), 503
    except json.JSONDecodeError:
        return jsonify({'error': 'Failed to parse LLM response'}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

if __name__ == '__main__':
    initialize_knowledge_base()
    app.run(debug=True, port=5000)
