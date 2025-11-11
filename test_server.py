"""
测试3: MCP 服务器测试
- 启动 MCP 服务器并暴露端口
- 提供 HTTP 接口供外部工具测试
- 使用标准 MCP 协议通信
"""

import subprocess
import time
import requests
import sys
import os

print("=" * 70)
print("🖥️  测试3: MCP 服务器测试")
print("=" * 70)

# 服务器配置
SERVER_SCRIPT = "server.py"
VENV_PYTHON = ".venv\\Scripts\\python.exe" if sys.platform == "win32" else ".venv/bin/python"
TEST_PORT = 8080  # server.py 中配置的端口


def start_server():
    """启动 MCP 服务器"""
    print("\n🚀 启动 MCP 服务器...")
    print(f"   命令: {VENV_PYTHON} {SERVER_SCRIPT}")
    print(f"   端口: {TEST_PORT}")
    print("-" * 70)
    
    try:
        # 启动服务器进程
        process = subprocess.Popen(
            [VENV_PYTHON, SERVER_SCRIPT],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        print("⏳ 等待服务器启动...")
        time.sleep(8)  # 等待模型加载
        
        if process.poll() is not None:
            # 进程已退出
            stdout, stderr = process.communicate()
            print(f"❌ 服务器启动失败")
            print(f"输出: {stdout}")
            print(f"错误: {stderr}")
            return None
        
        print("✅ 服务器已启动")
        return process
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return None


def test_mcp_protocol():
    """测试 MCP 协议（stdio 通信）"""
    print("\n" + "=" * 70)
    print("📡 测试 MCP 协议")
    print("-" * 70)
    print("💡 MCP 使用 stdio 通信，不是 HTTP 协议")
    print("   可以通过以下方式测试:")
    print()
    print("   1. 在 Cursor/Claude Desktop 中配置:")
    print("      {")
    print("        \"mcpServers\": {")
    print("          \"rag-app\": {")
    print(f"            \"command\": \"{os.path.abspath(VENV_PYTHON)}\",")
    print(f"            \"args\": [\"{os.path.abspath(SERVER_SCRIPT)}\"]")
    print("          }")
    print("        }")
    print("      }")
    print()
    print("   2. 使用 MCP Inspector:")
    print(f"      npx @modelcontextprotocol/inspector {VENV_PYTHON} {SERVER_SCRIPT}")
    print()
    print("   3. 使用 Python MCP 客户端测试 (见下方)")
    print("=" * 70)


def test_with_mcp_client():
    """使用 MCP 客户端库测试"""
    print("\n" + "=" * 70)
    print("🧪 Python MCP 客户端测试示例")
    print("-" * 70)
    
    example_code = '''
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 连接到服务器
server_params = StdioServerParameters(
    command=".venv\\\\Scripts\\\\python.exe",
    args=["server.py"],
)

async def test_tools():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化
            await session.initialize()
            
            # 列出可用工具
            tools = await session.list_tools()
            print("可用工具:", tools)
            
            # 调用工具
            result = await session.call_tool(
                "machine_learning_faq_retrieval_tool",
                arguments={"query": "What is supervised learning?"}
            )
            print("工具结果:", result)

# 运行测试
import asyncio
asyncio.run(test_tools())
'''
    
    print("💡 示例代码（需要安装 mcp 客户端）:")
    print(example_code)
    print("=" * 70)


def show_simple_test():
    """显示简单测试方法"""
    print("\n" + "=" * 70)
    print("✅ 服务器运行中")
    print("=" * 70)
    print("\n📝 测试方法:")
    print("\n1️⃣  使用 MCP Inspector (推荐)")
    print("   npx @modelcontextprotocol/inspector .venv\\Scripts\\python.exe server.py")
    print("   浏览器访问: http://localhost:5173")
    print()
    print("2️⃣  在 Cursor 中配置 mcp.json")
    print("   然后在 Cursor 聊天中使用工具")
    print()
    print("3️⃣  使用 Claude Desktop")
    print("   配置 claude_desktop_config.json")
    print()
    print("⏸️  按 Ctrl+C 停止服务器")
    print("=" * 70)


if __name__ == "__main__":
    # 启动服务器
    server_process = start_server()
    
    if server_process:
        try:
            # 显示测试信息
            test_mcp_protocol()
            test_with_mcp_client()
            show_simple_test()
            
            # 保持服务器运行
            print("\n⏳ 服务器运行中，等待测试...")
            server_process.wait()
            
        except KeyboardInterrupt:
            print("\n\n🛑 停止服务器...")
            server_process.terminate()
            server_process.wait()
            print("✅ 服务器已停止")
        
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            server_process.terminate()
    
    else:
        print("\n" + "=" * 70)
        print("💡 提示:")
        print("   如果启动失败，可以手动运行:")
        print(f"   {VENV_PYTHON} {SERVER_SCRIPT}")
        print("=" * 70)
