"""
测试1: 本地直接测试（最简单）
- 测试向量检索功能
- 测试 Web 搜索功能
- 配合 Ollama 进行 RAG 问答
- 不需要启动 server.py
"""

import os
import requests
from dotenv import load_dotenv
from rag_app import Retriever, QdrantVDB, EmbedData

load_dotenv()

print("=" * 70)
print("🧪 测试1: 本地直接测试")
print("=" * 70)

# 初始化 RAG
print("\n📚 初始化向量数据库...")
embed = EmbedData()
vdb = QdrantVDB(collection="ml_faq_collection", vector_size=embed.dim)
retriever = Retriever(vdb, embed)
print("✅ 初始化完成\n")


# ========== 测试1: 向量检索 ==========
print("=" * 70)
print("测试 A: 向量检索")
print("-" * 70)

queries = ["What is supervised learning?", "How to prevent overfitting?"]
for q in queries:
    print(f"\n❓ {q}")
    result = retriever.search(q, k=2)
    print(f"📝 {result[:150]}...\n")


# ========== 测试2: Web 搜索 ==========
print("=" * 70)
print("测试 B: Web 搜索（可选）")
print("-" * 70)

api_key = os.getenv("SERPER_API_KEY")
if api_key:
    try:
        resp = requests.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
            json={"q": "machine learning 2024", "num": 2},
            timeout=10
        )
        print(f"\n🔍 搜索结果:")
        for item in resp.json().get("organic", [])[:2]:
            print(f"  • {item.get('title', '')}")
    except Exception as e:
        print(f"❌ {e}")
else:
    print("⚠️  未配置 SERPER_API_KEY，跳过")


# ========== 测试3: Ollama RAG 问答 ==========
print("\n" + "=" * 70)
print("测试 C: Ollama RAG 问答（需要 Ollama）")
print("-" * 70)

def rag_chat(question: str, model: str = "qwen2.5:7b-instruct"):
    """RAG + Ollama 问答"""
    context = retriever.search(question, k=2)
    prompt = f"基于以下知识回答:\n{context}\n\n问题: {question}\n回答:"
    
    try:
        resp = requests.post(
            'http://localhost:11434/api/generate',
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=60
        )
        return resp.json().get('response', '').strip()
    except:
        return "❌ Ollama 未运行或连接失败"

question = "什么是监督学习？"
print(f"\n❓ {question}")
answer = rag_chat(question)
print(f"💡 {answer[:200]}...\n")

print("=" * 70)
print("✅ 测试完成")
print("=" * 70)
