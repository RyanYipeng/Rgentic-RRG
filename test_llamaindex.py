"""
测试2: LlamaIndex Agent 测试
- 使用 LlamaIndex Agent 自动选择工具
- 配合 Ollama 模型进行智能问答
- 不需要启动 server.py
"""

from llama_index.core import Settings, PromptTemplate
from llama_index.llms.ollama import Ollama
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent

# 导入 MCP 工具的核心功能（不启动服务器）
from rag_app import Retriever, QdrantVDB, EmbedData
import os
import requests
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("🚀 LlamaIndex + Ollama + MCP RAG 工具集成")
print("=" * 70)

# ==========================================
# 1. 初始化 Ollama LLM
# ==========================================
print("\n🤖 初始化 Ollama 模型...")
llm = Ollama(
    model="qwen2.5:7b-instruct",
    base_url="http://localhost:11434",
    temperature=0.7,
    request_timeout=120.0,
)
Settings.llm = llm

print("✅ Ollama 模型加载完成: qwen2.5:7b-instruct\n")

# ==========================================
# 2. 初始化 RAG 组件
# ==========================================
print("📚 初始化向量数据库...")
embed = EmbedData()
vdb = QdrantVDB(collection="ml_faq_collection", vector_size=embed.dim)
retriever = Retriever(vdb, embed)
print("✅ 向量数据库初始化完成\n")

# ==========================================
# 3. 将 MCP 工具包装为 LlamaIndex 工具
# ==========================================

def ml_faq_tool(query: str) -> str:
    """
    检索机器学习 FAQ 知识库。
    当用户询问机器学习、深度学习、数据科学相关问题时使用此工具。
    
    Args:
        query: 用户的问题
        
    Returns:
        str: 相关的 FAQ 答案
    """
    return retriever.search(query, k=3)


def web_search_tool(query: str, num_results: int = 5) -> str:
    """
    使用 Serper.dev 搜索网络获取最新信息。
    当问题需要最新信息、新闻、或超出知识库范围时使用。
    
    Args:
        query: 搜索关键词
        num_results: 返回结果数量
        
    Returns:
        str: 搜索结果摘要
    """
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        return "未配置 SERPER_API_KEY，无法使用网络搜索"
    
    try:
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
            results.append(f"标题: {title}\n链接: {link}\n摘要: {snippet}\n")
        return "\n".join(results) if results else "未找到相关结果"
    except Exception as e:
        return f"搜索失败: {str(e)}"


# 创建 LlamaIndex 工具
ml_tool = FunctionTool.from_defaults(fn=ml_faq_tool)
search_tool = FunctionTool.from_defaults(fn=web_search_tool)

print("🔧 工具注册完成:")
print("  - ml_faq_tool: 机器学习知识库检索")
print("  - web_search_tool: 网络搜索")
print()

# ==========================================
# 4. 创建 ReAct Agent
# ==========================================
print("🧠 创建 ReAct Agent...")
agent = ReActAgent.from_tools(
    tools=[ml_tool, search_tool],
    llm=llm,
    verbose=True,
    max_iterations=5,
)
print("✅ Agent 创建完成\n")

# ==========================================
# 5. 测试问答
# ==========================================

test_questions = [
    "什么是监督学习？它有哪些应用场景？",
    "如何避免机器学习模型过拟合？",
    "交叉验证的原理是什么？",
]

print("=" * 70)
print("📝 开始测试问答")
print("=" * 70)

for i, question in enumerate(test_questions, 1):
    print(f"\n{'=' * 70}")
    print(f"问题 {i}: {question}")
    print('=' * 70)
    
    try:
        response = agent.chat(question)
        print(f"\n🤖 回答:\n{response}\n")
    except Exception as e:
        print(f"❌ 错误: {e}\n")

print("=" * 70)
print("✅ 测试完成！")
print("=" * 70)
print("\n💡 提示：Agent 会自动选择合适的工具来回答问题")
print("   - ML 相关问题 → 使用 ml_faq_tool")
print("   - 需要最新信息 → 使用 web_search_tool")
print("   - 可以在 verbose=True 模式下看到工具调用过程")
