import os
import json
from typing import Any

from azure.core.credentials import AzureKeyCredential
from azure.core.pipeline.transport import RequestsTransport
from azure.search.documents import SearchClient
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from openai import AzureOpenAI
import requests

load_dotenv()

app = Flask(__name__)

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-5")

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT", "")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY", "")
AZURE_SEARCH_INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME", "house-rent-index")
AZURE_SEARCH_VERIFY_SSL = os.getenv("AZURE_SEARCH_VERIFY_SSL", "true").lower() != "false"

POLICY_KNOWLEDGE_BASE = """
IT Policy:
- Use company-approved devices and software for official work.
- Do not share confidential data through personal email or public file sharing tools.
- Report lost devices, suspicious links, or security incidents immediately to IT support.

Password Change Policy:
- Change passwords every 90 days or immediately if compromise is suspected.
- Use at least 12 characters with uppercase, lowercase, number, and symbol combinations.
- Do not reuse old passwords or share passwords with anyone.
- Enable multi-factor authentication wherever available.

Acceptable Use Policy:
- Company systems should be used for business purposes and approved learning activities.
- Do not install unauthorized applications or bypass security controls.
- Internet usage must comply with legal, ethical, and company security standards.

Data Protection Policy:
- Classify sensitive data before storing or sharing it.
- Store business documents only in approved cloud storage locations.
- Share data using least-privilege access and remove access when no longer needed.
"""


def get_openai_client() -> AzureOpenAI:
    missing = [
        name
        for name, value in {
            "AZURE_OPENAI_ENDPOINT": AZURE_OPENAI_ENDPOINT,
            "AZURE_OPENAI_API_KEY": AZURE_OPENAI_API_KEY,
            "AZURE_OPENAI_DEPLOYMENT": AZURE_OPENAI_DEPLOYMENT,
        }.items()
        if not value
    ]
    if missing:
        raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")

    return AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
    )


def ask_model(system_prompt: str, user_prompt: str) -> str:
    if AZURE_OPENAI_ENDPOINT.rstrip("/").endswith("/openai/v1/responses"):
        response = requests.post(
            AZURE_OPENAI_ENDPOINT,
            headers={"api-key": AZURE_OPENAI_API_KEY, "Content-Type": "application/json"},
            json={
                "model": AZURE_OPENAI_DEPLOYMENT,
                "instructions": system_prompt,
                "input": user_prompt,
                "max_output_tokens": 800,
                "reasoning": {"effort": "minimal"},
            },
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        if data.get("output_text"):
            return data["output_text"]

        output_parts = []
        for output_item in data.get("output", []):
            for content_item in output_item.get("content", []):
                text = content_item.get("text")
                if text:
                    output_parts.append(text)
        return "\n".join(output_parts) or "No response generated."

    client = get_openai_client()
    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_completion_tokens=800,
    )
    return response.choices[0].message.content or "No response generated."


def search_house_rent_dataset(query: str) -> list[dict[str, Any]]:
    if not AZURE_SEARCH_ENDPOINT or not AZURE_SEARCH_KEY or not AZURE_SEARCH_INDEX_NAME:
        raise RuntimeError(
            "Configure AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_KEY, and AZURE_SEARCH_INDEX_NAME "
            "to use the House Rent Prediction Agent."
        )

    search_client = SearchClient(
        endpoint=AZURE_SEARCH_ENDPOINT,
        index_name=AZURE_SEARCH_INDEX_NAME,
        credential=AzureKeyCredential(AZURE_SEARCH_KEY),
        transport=RequestsTransport(connection_verify=AZURE_SEARCH_VERIFY_SSL),
    )
    results = search_client.search(search_text=query, top=5)
    documents: list[dict[str, Any]] = []
    for result in results:
        documents.append({key: value for key, value in dict(result).items() if not key.startswith("@search")})
    return documents


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/chat")
def chat_app():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "Message is required."}), 400

    try:
        answer = ask_model(
            "You are a helpful GPT-5 chat assistant. Answer clearly and practically.",
            message,
        )
        return jsonify({"answer": answer})
    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.post("/api/policy-helper")
def policy_helper():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"error": "Policy question is required."}), 400

    try:
        answer = ask_model(
            "You are a Policy Helper Agent. Answer only from the provided policy context. "
            "If the context does not contain the answer, say that HR or IT should be contacted.",
            f"Policy context:\n{POLICY_KNOWLEDGE_BASE}\n\nUser question: {question}",
        )
        return jsonify({"answer": answer})
    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.post("/api/house-rent")
def house_rent_prediction():
    data = request.get_json(silent=True) or {}
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "House rent query is required."}), 400

    try:
        documents = search_house_rent_dataset(query)
        answer = ask_model(
            "You are a House Rent Prediction Agent. Answer in 2-3 sentences using only the provided dataset rows.",
            "User query: "
            f"{query}\n\nDataset rows from Azure AI Search:\n{json.dumps(documents, indent=2)}\n\n"
            "Give an estimated monthly rent and mention the closest matching row.",
        )
        return jsonify({"answer": answer, "search_results": documents})
    except Exception as error:
        return jsonify({"error": str(error)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")), debug=True)