# 🍒 Cherry Studio 测试 MCP 完整流程

## 📌 前提条件

- ✅ 已安装 [Cherry Studio](https://github.com/kangfenmao/cherry-studio)
- ✅ 已安装 Python 和项目依赖
- ✅ Ollama 正在运行（可选，看你用什么模型）

---

## 🚀 快速开始（3步）

### 第 1 步：配置 Cherry Studio 的 MCP 服务器

Cherry Studio 的 MCP 配置文件位置：

设置-MCP-右上角添加-从Json导入-将以下内容粘贴过去（注意项目路径修改）
```json
{
  "mcpServers": {
    "rag-ml-assistant": {
      "command": "项目路径\\.venv\\Scripts\\python.exe",
      "args": ["项目路径\\server.py"],
      "env": {}
    }
  }
}
```

**⚠️ 重要：**
- 路径必须使用**绝对路径**
- Windows 路径使用 `\\` 双反斜杠
- 确保 Python 路径指向虚拟环境中的 Python

---

### 第 2 步：启动 Cherry Studio 并加载 MCP 工具

1. **打开 Cherry Studio**

2. **检查 MCP 工具加载状态**
   - 进入设置 → MCP 服务器
   - 查看 `rag-ml-assistant` 是否显示为 ✅ 已连接
   - 如果显示错误，检查日志

3. **查看可用工具**
   - 在 Cherry Studio 中应该能看到两个工具：
     - `machine_learning_faq_retrieval_tool` - ML知识库检索
     - `serper_web_search_tool` - 网络搜索

---

### 第 3 步：测试工具调用

#### 测试 1: ML 知识库检索

在 Cherry Studio 的对话框中输入：

```
什么是监督学习？请使用知识库工具查询。
```

**预期效果：**
- Cherry Studio 会自动调用 `machine_learning_faq_retrieval_tool`
- 返回知识库中的准确定义
- 可以在工具调用日志中看到调用记录

#### 测试 2: 网络搜索（需要 API Key）

```
查询一下 Python 3.13 的最新特性
```

**预期效果：**
- Cherry Studio 会调用 `serper_web_search_tool`
- 返回最新的搜索结果
- 如果未配置 `SERPER_API_KEY`，会提示需要配置

---



### 完整配置示例

```json
{
  "mcpServers": {
    "rag-ml-assistant": {
      "command": "D:\\Projects\\MCP\\Rgentic RRG\\.venv\\Scripts\\python.exe",
      "args": ["D:\\Projects\\MCP\\Rgentic RRG\\server.py"],
      "env": {
        "SERPER_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**说明：**
- `command`: Python 解释器路径（虚拟环境）
- `args`: server.py 的绝对路径
- `env`: 环境变量（可选，用于传递 API Key）

---

### 环境变量配置（网络搜索）

**方法 1: 在 .env 文件中配置**（推荐）

编辑项目根目录的 `.env` 文件：
```bash
SERPER_API_KEY=your_api_key_here
```

**方法 2: 在 mcp_servers.json 中配置**

```json
{
  "mcpServers": {
    "rag-ml-assistant": {
      "command": "...",
      "args": ["..."],
      "env": {
        "SERPER_API_KEY": "your_actual_api_key"
      }
    }
  }
}
```

获取 API Key: https://serper.dev（有免费额度）

---

## 🐛 常见问题

### 1. MCP 服务器显示"未连接"

**解决方案：**
```powershell
# 检查 Python 路径是否正确
D:\Projects\MCP\Rgentic RRG\.venv\Scripts\python.exe --version

# 手动测试 server.py 是否能运行
D:\Projects\MCP\Rgentic RRG\.venv\Scripts\python.exe D:\Projects\MCP\Rgentic RRG\server.py
```

### 2. 工具不显示或无法调用

**检查清单：**
- [ ] server.py 是否正常运行
- [ ] 路径是否使用绝对路径
- [ ] Python 是否指向虚拟环境
- [ ] Cherry Studio 是否已重启

### 3. 网络搜索工具返回错误

**原因：**
- 未配置 `SERPER_API_KEY`

**解决：**
1. 访问 https://serper.dev 注册
2. 获取免费 API Key
3. 在 `.env` 文件中配置

### 4. 查看详细日志

Cherry Studio 日志位置：
```
%APPDATA%\cherry-studio\logs\
```

查看最新日志：
```powershell
Get-Content $env:APPDATA\cherry-studio\logs\main.log -Tail 50
```

---

## 📊 测试对比

### 使用 MCP 工具 vs 不使用工具

**示例对话：**

```
问题：什么是交叉验证？

不使用工具的回答：
交叉验证是机器学习中的一种评估方法...（通用回答）

使用 MCP 工具后：
[调用 machine_learning_faq_retrieval_tool]
交叉验证将数据集分为多个子集，用于估算模型的泛化性能...
（来自知识库的精确定义）
```

**如何确认工具被调用：**
- Cherry Studio 会在对话中显示工具调用标记
- 可以在设置中查看工具调用日志
- 回答内容会更加精确和具体

---

## 🎯 高级测试

### 测试场景 1: 知识库问答

```
请告诉我以下概念的区别：
1. 监督学习
2. 无监督学习
3. 强化学习
```

**预期：** 自动调用知识库工具，返回准确定义

### 测试场景 2: 实时信息查询

```
搜索一下最新的 AI 新闻
```

**预期：** 调用网络搜索工具，返回最新资讯

### 测试场景 3: 混合使用

```
根据知识库解释什么是深度学习，然后搜索一下最新的深度学习应用案例
```

**预期：** 
1. 先调用知识库工具获取定义
2. 再调用搜索工具获取最新案例
3. 综合两个来源给出完整回答

---

## 💡 使用技巧

### 1. 明确指示使用工具

```
使用知识库查询：什么是过拟合？
搜索一下：PyTorch 2.0 新特性
```

### 2. 让 AI 自动选择

```
告诉我关于机器学习的最新进展
```
AI 会根据问题自动决定是否需要工具

### 3. 验证工具效果

```
先不用工具回答这个问题，然后用工具再回答一次
```

---

## 📚 相关文档

- [Cherry Studio 官方文档](https://github.com/kangfenmao/cherry-studio)
- [MCP 协议说明](https://modelcontextprotocol.io/)
- 项目 README.md

---

## ✅ 快速检查清单

配置前：
- [ ] Cherry Studio 已安装
- [ ] 项目依赖已安装
- [ ] 虚拟环境已激活

配置时：
- [ ] 使用绝对路径
- [ ] Python 指向虚拟环境
- [ ] 路径使用正确的分隔符

测试时：
- [ ] Cherry Studio 已重启
- [ ] MCP 服务器显示"已连接"
- [ ] 可以看到两个工具
- [ ] 工具能正常调用

---

**🎉 配置完成后，你就可以在 Cherry Studio 中享受 MCP 增强的 AI 对话了！**
