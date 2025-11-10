# MCP-driven Agentic RAG (Vector DB + Web Search)

This demo shows a simple MCP server that exposes **two tools**:
1) `machine_learning_faq_retrieval_tool` — retrieves relevant ML FAQ answers from a Qdrant vector DB.
2) `bright_data_web_search_tool` — falls back to Bright Data SERP for general queries.

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # then put your Bright Data credentials
python server.py
```

## Add to Cursor

Open **Settings → MCP → Add new global MCP server**, then add the contents of `mcp.json`
(adjust the absolute path). You should see the server appear with the two tools.

## Try it

- Ask something ML-related (e.g., *what is supervised learning?*) → vector DB tool is picked.
- Ask a general question (e.g., *latest news about data lakes*) → Bright Data tool is picked.
