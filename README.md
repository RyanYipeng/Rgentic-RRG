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
├── server.py                      # MCP 服务器
├── rag_app/                       # RAG 核心模块
│   ├── data.py                   # 数据和 Embedding
│   ├── vdb.py                    # Qdrant 向量数据库
│   └── retriever.py              # 检索器
├── test_llamaindex.py            # 交互式测试
└── Cherry_Studio_配置指南.md     # Cherry Studio 集成教程
```

## 🧪 本地测试

### 交互式对比测试
需安装ollama并使用ollam pull 模型名称  来下载对应模型。
注意修改文件中自己下载的模型名称
```bash
.venv\Scripts\python test_llamaindex.py
```
**特点：**
- 🎯 **交互式输入**：你输入问题，实时看结果
- 📊 **三种对比**：每个问题展示3种回答方式
  - 纯 LlamaIndex LLM（不使用工具）
  - RAG 工具增强（使用知识库）
  - 网络搜索增强（使用最新信息）
- ✅ 清楚展示工具调用效果
- ❌ 不需要启动 server.py

## 🔧 集成到 AI 应用

### Cherry Studio（推荐）

完整配置教程请查看：**[Cherry_Studio_配置指南.md](./Cherry_Studio_配置指南.md)**

**快速配置：**
1. 打开 Cherry Studio 配置文件：`%APPDATA%\cherry-studio\mcp_servers.json`
2. 添加配置：
```json
{
  "mcpServers": {
    "rag-ml-assistant": {
      "command": "项目路径\\.venv\\Scripts\\python.exe",
      "args": ["项目路径\\server.py"]
    }
  }
}
```

### Cursor / Claude Desktop

在对应的配置文件中添加相同的 MCP 配置即可。

## 🛠️ 核心功能

### 1. 机器学习知识库检索（RAG 工具）
- 📚 向量数据库存储 FAQ
- 🔍 语义相似度搜索
- 💡 提供专业领域知识
- ✅ 两个测试都支持

### 2. Web 搜索工具
- 🌐 使用 Serper.dev API 搜索网络
- 📰 获取最新信息和新闻
- 🔑 需要配置 `SERPER_API_KEY`（在 .env 文件中）
- ✅ 两个测试都支持

**配置方法：**
```bash
# 复制示例文件
cp .env.example .env

# 编辑 .env 文件，添加你的 API Key
SERPER_API_KEY=your_api_key_here
```

**获取 API Key：**
访问 [serper.dev](https://serper.dev) 注册并获取免费 API Key

## 💡 使用场景

| 场景 | 是否需要 server.py | 方式 | 说明 |
|------|-------------------|------|------|
| 本地测试验证 | ❌ | test_llamaindex.py | 交互式三种对比 |
| Cherry Studio | ✅ | MCP 配置 | 推荐方式 |
| Cursor | ✅ | MCP 配置 | 自动工具调用 |
| Claude Desktop | ✅ | MCP 配置 | 自动工具调用 |

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
