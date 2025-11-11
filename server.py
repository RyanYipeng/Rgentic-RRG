from __future__ import annotations

import os
import json
import urllib.parse
import requests
from dotenv import load_dotenv

from mcp.server.fastmcp import FastMCP

# Rag components
from rag_app import Retriever, QdrantVDB, EmbedData

# ---------------------
# 1) Define the MCP server
# ---------------------

mcp = FastMCP(
    "Rgentic RRG",
    host="127.0.0.1",
    port=8080,
)

load_dotenv()  # load .env if present


# ---------------------
# 2) Vector DB MCP Tool
# ---------------------

# Build the retriever (Qdrant + Sentence-Transformers)
_embed = EmbedData()
_vdb = QdrantVDB(collection="ml_faq_collection", vector_size=_embed.dim)
_retriever = Retriever(_vdb, _embed)


@mcp.tool()
def machine_learning_faq_retrieval_tool(query: str) -> str:
    """Retrieve the most relevant documents from the machine learning FAQ collection.

    Use this tool when the user asks about **machine learning** topics.

    Input:
        query: str -> The user's natural language query.
    Output:
        response: str -> Top-k relevant Q/A snippets from a Qdrant vector DB.
    """
    if not isinstance(query, str):
        raise ValueError("query must be a string")

    return _retriever.search(query)


# ---------------------
# 3) Web Search MCP Tool (Bright Data)
# ---------------------

@mcp.tool()
def serper_web_search_tool(query: str, num_results: int = 10) -> list[str]:
    """
    Search the web using Serper.dev (Google SERP API).

    Inputs:
        query: str -> what to search for
        num_results: int -> number of results (default 10)
    Output:
        list[str] -> "<title> — <url>\n<snippet>"
    """
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise RuntimeError("Missing SERPER_API_KEY in .env file.")

    resp = requests.post(
        "https://google.serper.dev/search",
        headers={
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        },
        json={"q": query, "num": num_results},
        timeout=15
    )
    data = resp.json()
    results = []
    for item in data.get("organic", [])[:num_results]:
        title = item.get("title", "")
        link = item.get("link", "")
        snippet = item.get("snippet", "")
        results.append(f"{title} — {link}\n{snippet}")
    return results


# ---------------------
# Run the server
# ---------------------

if __name__ == "__main__":
    # The FastMCP helper starts an HTTP server on host/port and exposes the tools.
    mcp.run()
