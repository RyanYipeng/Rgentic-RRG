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
    "MCP-RAG-app",
    host="127.0.0.1",
    port=8080,
    timeout=30,  # seconds
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
def bright_data_web_search_tool(query: str, num_results: int = 10) -> list[str]:
    """Search the web at scale using Bright Data's SERP proxy.

    Use this tool for **general or non-ML** queries to gather fresh context
    from multiple sources via Bright Data's super proxy.

    Inputs:
        query: str -> What to search for.
        num_results: int -> How many organic results to return (default 10).

    Output:
        context: list[str] -> A list of strings formatted as: "<title> — <url>\n<snippet>"
    """
    if not isinstance(query, str):
        raise ValueError("query must be a string")

    host = os.getenv("BRIGHT_DATA_HOST", "brd.superproxy.io")
    port = int(os.getenv("BRIGHT_DATA_PORT", "33335"))
    username = os.getenv("BRIGHT_DATA_USERNAME")
    password = os.getenv("BRIGHT_DATA_PASSWORD")

    if not username or not password:
        raise RuntimeError(
            "Missing Bright Data credentials. Please set BRIGHT_DATA_USERNAME and BRIGHT_DATA_PASSWORD in your environment (.env)."
        )

    proxy = f"http://{username}:{password}@{host}:{port}"
    q = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={q}&num={num_results}&brd_json=1"

    # Note: Bright Data returns JSON when `brd_json=1` is present.
    resp = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=30, verify=False)
    data = resp.json()

    # Parse organic results
    organic = data.get("organic", []) or []
    results = []
    for item in organic[:num_results]:
        title = item.get("title") or ""
        link = item.get("url") or ""
        snippet = item.get("snippet") or item.get("description") or ""
        results.append(f"{title} — {link}\n{snippet}")
    return results


# ---------------------
# Run the server
# ---------------------

if __name__ == "__main__":
    # The FastMCP helper starts an HTTP server on host/port and exposes the tools.
    mcp.run()
