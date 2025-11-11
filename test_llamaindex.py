"""
测试2: LlamaIndex 对比测试
- 使用 LlamaIndex 的 Ollama LLM
- 对比纯模型回答和 RAG 工具增强回答
- 展示工具调用的效果
- 不需要启动 server.py
"""

from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from rag_app import Retriever, QdrantVDB, EmbedData
import os
import requests
from dotenv import load_dotenv

load_dotenv()

MODEL = "qwen2.5:7b-instruct"   

print("=" * 80)
print("🧪 测试2: LlamaIndex 对比测试")
print("=" * 80)

# 初始化 LlamaIndex Ollama LLM
print("\n🤖 初始化 LlamaIndex Ollama LLM...")
llm = Ollama(
    model=MODEL,
    base_url="http://localhost:11434",
    temperature=0.7,
    request_timeout=120.0,
)
Settings.llm = llm
print("✅ LLM 就绪\n")

# 初始化 RAG 工具
print("📚 初始化 RAG 工具...")
embed = EmbedData()
vdb = QdrantVDB(collection="ml_faq_collection", vector_size=embed.dim)
retriever = Retriever(vdb, embed)
print("✅ RAG 工具就绪\n")


def pure_llama_answer(question: str) -> str:
    """纯 LlamaIndex LLM 回答（不使用工具）"""
    prompt = f"请用中文简洁回答：{question}"
    response = llm.complete(prompt)
    return str(response).strip()


def rag_llama_answer(question: str) -> str:
    """使用 RAG 工具 + LlamaIndex LLM 回答"""
    # 使用 RAG 工具检索知识库
    context = retriever.search(question, k=2)
    
    # 构造带上下文的提示词
    prompt = f"""基于以下知识库内容回答问题：

【知识库】
{context}

【问题】
{question}

【要求】请用中文简洁回答

【回答】"""
    
    response = llm.complete(prompt)
    return str(response).strip()


def web_search(query: str, num: int = 3) -> str:
    """网络搜索工具"""
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        return "⚠️ 未配置 SERPER_API_KEY，无法使用网络搜索"
    
    try:
        resp = requests.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
            json={"q": query, "num": num},
            timeout=10
        )
        results = resp.json().get("organic", [])
        if not results:
            return "未找到搜索结果"
        
        output = []
        for i, item in enumerate(results[:num], 1):
            output.append(f"{i}. {item.get('title', '')}")
            output.append(f"   {item.get('snippet', '')}")
            output.append(f"   {item.get('link', '')}")
        return "\n".join(output)
    except Exception as e:
        return f"❌ 搜索失败: {e}"


def web_search_llama_answer(question: str) -> str:
    """使用网络搜索 + LlamaIndex LLM 回答"""
    # 1. 使用网络搜索获取信息
    search_results = web_search(question, num=2)
    
    # 2. 将搜索结果提供给 LlamaIndex LLM
    prompt = f"""基于以下网络搜索结果回答问题：

【搜索结果】
{search_results}

【问题】
{question}

【要求】请用中文简洁回答，综合搜索结果的信息

【回答】"""
    
    response = llm.complete(prompt)
    return str(response).strip()


# 交互式测试
print("=" * 80)
print("📝 开始交互式对比测试")
print("=" * 80)
print("\n💡 提示：")
print("   1. 输入问题进行测试")
print("   2. 输入 'quit' 或 'exit' 退出")
print("   3. 每个问题会展示三种回答：")
print("      - 纯 LlamaIndex LLM（不使用工具）")
print("      - RAG 工具增强（使用知识库）")
print("      - 网络搜索增强（使用最新信息）")
print("\n" + "=" * 80)

question_count = 0

while True:
    print("\n" + "─" * 80)
    question = input("\n❓ 请输入你的问题: ").strip()
    
    if not question:
        print("⚠️  问题不能为空，请重新输入")
        continue
    
    if question.lower() in ['quit', 'exit', '退出', 'q']:
        print("\n👋 退出测试")
        break
    
    question_count += 1
    print(f"\n{' 问题 ' + str(question_count) + ' ':=^80}")
    print(f"❓ {question}\n")
    
    # 1. 纯 LlamaIndex LLM 回答
    print("┌─ 🤖 纯 LlamaIndex LLM 回答（不使用工具）")
    print("│")
    try:
        pure_answer = pure_llama_answer(question)
        for line in pure_answer.split('\n'):
            print(f"│  {line}")
    except Exception as e:
        print(f"│  ❌ 错误: {e}")
    print("└" + "─" * 78)
    
    print("")
    
    # 2. RAG 增强回答
    print("┌─ 🔧 RAG 工具 + LlamaIndex LLM（使用知识库）")
    print("│")
    try:
        rag_answer = rag_llama_answer(question)
        for line in rag_answer.split('\n'):
            print(f"│  {line}")
    except Exception as e:
        print(f"│  ❌ 错误: {e}")
    print("└" + "─" * 78)
    
    print("")
    
    # 3. 网络搜索增强回答
    print("┌─ 🌐 网络搜索 + LlamaIndex LLM（使用最新信息）")
    print("│")
    try:
        web_answer = web_search_llama_answer(question)
        for line in web_answer.split('\n'):
            print(f"│  {line}")
    except Exception as e:
        print(f"│  ❌ 错误: {e}")
    print("└" + "─" * 78)
    
    print("\n💡 对比说明：")
    print("   • 第1个：纯 LlamaIndex LLM（基于训练数据）")
    print("   • 第2个：RAG 工具（基于本地知识库）")
    print("   • 第3个：网络搜索（基于实时信息）")

print("\n" + "=" * 80)
print(f"✅ 测试完成！共测试了 {question_count} 个问题")
print("=" * 80)
print("\n📊 总结：")
print("   ✓ 可以清楚看到三种方式的区别")
print("   ✓ RAG 工具提供知识库中的精确信息")
print("   ✓ 网络搜索提供最新的实时信息")
print("   ✓ 纯 LLM 回答较为通用")
print("")
