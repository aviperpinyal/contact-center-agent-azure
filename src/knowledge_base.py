"""Retrieval from the Foundry IQ knowledge base (Azure AI Search agentic retrieval).

Keyless: uses your Azure CLI sign-in (Entra ID). Requires the Search Index Data Reader
(or Contributor) role on the Search service.
"""

import json
import os

import requests
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

API_VERSION = "2026-11-01-preview"
SEARCH_ENDPOINT = os.environ["SEARCH_ENDPOINT"].rstrip("/")
KNOWLEDGE_BASE = os.getenv("KNOWLEDGE_BASE", "contoso-support-kb")

# Cap on passages sent to the agent (keeps prompts small). Relevance threshold tuning comes in Milestone 3.
MAX_PASSAGES = 5

_credential = AzureCliCredential()


def retrieve(query: str) -> list[dict]:
    """Ask the knowledge base for passages relevant to `query`.

    Returns a list of {"source", "score", "content"} sorted by relevance, highest first.
    """
    token = _credential.get_token("https://search.azure.com/.default").token
    response = requests.post(
        f"{SEARCH_ENDPOINT}/knowledgebases/{KNOWLEDGE_BASE}/retrieve?api-version={API_VERSION}",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"messages": [{"role": "user", "content": [{"type": "text", "text": query}]}]},
        timeout=60,
    )
    response.raise_for_status()
    result = response.json()

    # Map each reference id to its source file name and reranker score.
    refs = {}
    for ref in result.get("references", []):
        source = (ref.get("blobUrl") or "unknown").rsplit("/", 1)[-1]
        refs[str(ref.get("id"))] = {"source": source, "score": ref.get("rerankerScore") or 0.0}

    passages = []
    for item in result.get("response", []):
        for content in item.get("content", []):
            try:
                docs = json.loads(content.get("text", "[]"))
            except json.JSONDecodeError:
                continue
            for doc in docs:
                meta = refs.get(str(doc.get("ref_id")), {"source": "unknown", "score": 0.0})
                passages.append({**meta, "content": doc.get("content", "")})

    passages.sort(key=lambda p: p["score"], reverse=True)
    return passages[:MAX_PASSAGES]
