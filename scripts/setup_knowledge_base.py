"""Milestone 1, Step 5: create the Foundry IQ knowledge source and knowledge base, then test retrieval.

Keyless by design:
- This script signs in to Azure AI Search with your Azure CLI identity (Entra ID).
- The Search service reads Blob Storage and calls the models with its own managed identity.

Usage:
    python scripts/setup_knowledge_base.py                 # create/update everything, then run a test query
    python scripts/setup_knowledge_base.py "your question" # same, with your own test question

Safe to re-run: PUT requests create the object if it's missing and update it if it exists.
"""

import json
import os
import sys
import time

import requests
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

# Knowledge sources and knowledge bases are newer APIs; this preview version matches Microsoft's examples.
API_VERSION = "2026-11-01-preview"

SEARCH_ENDPOINT = os.environ["SEARCH_ENDPOINT"].rstrip("/")
AOAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/")
CHAT_MODEL = os.environ["FOUNDRY_MODEL"]
EMBED_MODEL = os.environ["EMBED_MODEL"]
STORAGE_RESOURCE_ID = os.environ["STORAGE_RESOURCE_ID"]

BLOB_CONTAINER = "kb-docs"
KNOWLEDGE_SOURCE = "contoso-kb-docs"
KNOWLEDGE_BASE = "contoso-support-kb"

DEFAULT_QUESTION = "Does alarm monitoring keep working if my home internet goes down?"

credential = AzureCliCredential()


def call(method: str, path: str, body: dict | None = None) -> dict:
    """Call the Azure AI Search REST API with an Entra ID token; stop with details on any error."""
    token = credential.get_token("https://search.azure.com/.default").token
    response = requests.request(
        method,
        f"{SEARCH_ENDPOINT}{path}?api-version={API_VERSION}",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=body,
        timeout=120,
    )
    if response.status_code >= 400:
        print(f"\n{method} {path} failed: HTTP {response.status_code}")
        print(response.text)
        sys.exit(1)
    return response.json() if response.content else {}


def model(deployment: str) -> dict:
    """A model reference. Deployment names match model names in this project."""
    return {
        "kind": "azureOpenAI",
        "azureOpenAIParameters": {
            "resourceUri": AOAI_ENDPOINT,
            "deploymentId": deployment,
            "modelName": deployment,
        },
    }


def create_knowledge_source() -> None:
    print(f"1. Creating knowledge source '{KNOWLEDGE_SOURCE}' (Blob container '{BLOB_CONTAINER}')...")
    call(
        "PUT",
        f"/knowledgesources/{KNOWLEDGE_SOURCE}",
        {
            "name": KNOWLEDGE_SOURCE,
            "kind": "azureBlob",
            "description": "Contoso Home Services support documentation: plans, monitoring, "
            "troubleshooting, outages, support hours, billing and privacy.",
            "azureBlobParameters": {
                # ResourceId= form means "connect with the Search service's managed identity" (no key).
                "connectionString": f"ResourceId={STORAGE_RESOURCE_ID};",
                "containerName": BLOB_CONTAINER,
                "ingestionParameters": {
                    "embeddingModel": model(EMBED_MODEL),
                    "chatCompletionModel": model(CHAT_MODEL),
                    "contentExtractionMode": "minimal",
                },
            },
        },
    )
    print("   Created. Search is now building a data source, index and indexer behind the scenes.")


def wait_for_ingestion(timeout_seconds: int = 900) -> None:
    print("2. Waiting for the documents to be ingested (chunked, embedded, indexed)...")
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        status = call("GET", f"/knowledgesources/{KNOWLEDGE_SOURCE}/status")
        last = status.get("lastSynchronizationState") or {}
        current = status.get("currentSynchronizationState") or {}
        if last.get("endTime"):
            print(f"   Finished: {json.dumps(last, indent=2)}")
            errors = current.get("errors") or []
            if errors:
                print(f"   Document errors: {json.dumps(errors, indent=2)}")
            return
        print(f"   Still running... ({status.get('synchronizationStatus', 'status unknown')})")
        time.sleep(15)
    print("   Timed out waiting. Last status:")
    print(json.dumps(status, indent=2))
    sys.exit(1)


def create_knowledge_base() -> None:
    print(f"3. Creating knowledge base '{KNOWLEDGE_BASE}'...")
    call(
        "PUT",
        f"/knowledgebases/{KNOWLEDGE_BASE}",
        {
            "name": KNOWLEDGE_BASE,
            "description": "Knowledge base for the Contoso Home Services customer support agent.",
            "retrievalInstructions": "Use the Contoso support documentation for questions about "
            "plans, prices, alarm monitoring, hub and device troubleshooting, outages, support hours, "
            "billing, cancellation, cameras and privacy.",
            "knowledgeSources": [{"name": KNOWLEDGE_SOURCE}],
            # The model plans sub-queries (low/medium reasoning effort).
            "models": [model(CHAT_MODEL)],
            # Return grounding passages, not a finished answer: the agent writes the answer in Step 6.
            "outputMode": "extractiveData",
            "retrievalReasoningEffort": {"kind": "low"},
        },
    )
    print("   Created.")


def test_retrieval(question: str) -> None:
    print(f"4. Test retrieval\n   Question: {question}\n")
    result = call(
        "POST",
        f"/knowledgebases/{KNOWLEDGE_BASE}/retrieve",
        {
            "messages": [{"role": "user", "content": [{"type": "text", "text": question}]}],
            "includeActivity": True,
        },
    )

    print("   What the knowledge base did (activity):")
    for step in result.get("activity", []):
        details = {k: v for k, v in step.items() if k in ("knowledgeSourceName", "count", "inputTokens", "outputTokens", "elapsedMs")}
        print(f"   - {step.get('type')}: {details}")

    print("\n   Grounding passages returned:")
    for item in result.get("response", []):
        for content in item.get("content", []):
            try:
                passages = json.loads(content.get("text", "[]"))
            except json.JSONDecodeError:
                print(f"   {content.get('text', '')[:500]}")
                continue
            for passage in passages:
                preview = {k: (str(v)[:200] + "…" if len(str(v)) > 200 else v) for k, v in passage.items()}
                print(f"   - {json.dumps(preview, ensure_ascii=False)}")

    print(f"\n   References: {len(result.get('references', []))}")
    for ref in result.get("references", []):
        print(f"   - {json.dumps(ref, ensure_ascii=False)[:400]}")


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or DEFAULT_QUESTION
    create_knowledge_source()
    wait_for_ingestion()
    create_knowledge_base()
    test_retrieval(question)
