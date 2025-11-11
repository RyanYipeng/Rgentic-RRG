# MCP RAG 项目

基于 MCP 协议的 RAG（检索增强生成）应用，提供向量检索和网络搜索工具。

## 🚀 快速开始

```bash
# 1. 创建虚拟环境并安装依赖
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 2. 配置环境变量（可选）
copy .env.example .env
# 编辑 .env 添加 SERPER_API_KEY
```

## 📦 项目结构

```
├── server.py              # MCP 服务器（用于 Cursor/Claude 集成）
├── rag_app/               # RAG 核心模块
│   ├── data.py           # 数据和 Embedding
│   ├── vdb.py            # Qdrant 向量数据库
│   └── retriever.py      # 检索器
├── test_basic.py         # 测试1: 本地直接测试
├── test_llamaindex.py    # 测试2: LlamaIndex Agent
└── test_server.py        # 测试3: MCP 服务器测试
```

## 🧪 三种测试方式

### 测试1: 本地直接测试（最简单）
```bash
.venv\Scripts\python test_basic.py
```
- ✅ 测试向量检索
- ✅ 测试 Web 搜索
- ✅ 配合 Ollama 进行 RAG 问答
- ❌ 不需要启动 server.py

### 测试2: LlamaIndex Agent（智能问答）
```bash
# 需要先安装 LlamaIndex（已包含在 requirements.txt）
.venv\Scripts\python test_llamaindex.py
```
- ✅ 使用 Agent 自动选择工具
- ✅ 配合 Ollama 智能问答
- ❌ 不需要启动 server.py

### 测试3: MCP 服务器（跨应用集成）
```bash
.venv\Scripts\python test_server.py
```
- ✅ 启动 MCP 服务器
- ✅ 提供标准 MCP 协议接口
- ✅ 可被 Cursor/Claude 调用

## 🔧 集成到 Cursor/Claude

在 Cursor 或 Claude Desktop 中配置 `mcp.json`：

```json
{
  "mcpServers": {
    "rag-app": {
      "command": "D:\\Projects\\MCP\\Rgentic RRG\\.venv\\Scripts\\python.exe",
      "args": ["D:\\Projects\\MCP\\Rgentic RRG\\server.py"]
    }
  }
}
```

然后在 Cursor 聊天中询问机器学习相关问题，工具会自动被调用。

## 🛠️ 核心功能

### 1. 向量检索工具
- 检索机器学习 FAQ 知识库
- 使用 Qdrant 内存向量数据库
- Sentence Transformers 进行向量化

### 2. Web 搜索工具
- 使用 Serper.dev API 搜索网络
- 获取最新信息和新闻
- 需要配置 `SERPER_API_KEY`

## 💡 使用场景

| 场景 | 是否需要 server.py | 推荐测试脚本 |
|------|-------------------|-------------|
| 本地测试验证 | ❌ | test_basic.py |
| 开发调试 | ❌ | test_basic.py |
| 智能问答 | ❌ | test_llamaindex.py |
| Cursor 集成 | ✅ | test_server.py |
| Claude Desktop | ✅ | test_server.py |

## 📚 扩展开发

### 添加自定义数据
编辑 `rag_app/data.py` 中的 `ML_FAQ` 列表：

```python
ML_FAQ = [
    {"id": 1, "q": "你的问题", "a": "你的答案"},
    # 添加更多...
]
```

### 在自己的应用中使用
```python
from rag_app import Retriever, QdrantVDB, EmbedData

embed = EmbedData()
vdb = QdrantVDB(collection="my_collection", vector_size=embed.dim)
retriever = Retriever(vdb, embed)

result = retriever.search("你的问题", k=3)
print(result)
```

## 📖 依赖说明

- **核心依赖**：mcp, qdrant-client, sentence-transformers
- **LlamaIndex**：可选，仅 test_llamaindex.py 需要
- **Ollama**：可选，用于本地 LLM 推理

## ⚙️ 环境要求

- Python 3.10+
- Ollama（可选，用于测试）
- Node.js（可选，用于 MCP Inspector）
