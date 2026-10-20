"""我的第一个 LangGraph Agent：ReAct 循环 + 工具调用 + 记忆。

运行：python agent.py
"""
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver

from tools import calculator, kb_search

load_dotenv()  # 从 .env 文件读取 DEEPSEEK_API_KEY

# 1. 大脑：DeepSeek 模型（OpenAI 兼容接口，换模型只改这两行）
llm = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com",
    api_key=os.environ["DEEPSEEK_API_KEY"],  # 显式从 .env 读 Key，不硬编码
)

# 2. 工具箱：想加新能力，写个 @tool 函数加进这个列表即可
tools = [calculator, kb_search]

# 3. 组装 Agent
#    create_agent 就是 ReAct 循环的现成实现：
#    思考 -> 调用工具 -> 观察结果 -> 再思考，直到给出最终回答。
#    checkpointer 给 Agent 加上记忆：同一个 thread_id 内记得之前聊过什么。
SYSTEM = (
    "你是一个 Agent 学习助手，正在教一名零基础学生。"
    "能用知识库回答的概念先查知识库；需要计算就调用计算器。"
    "回答要通俗、简短。"
)
agent = create_agent(llm, tools, system_prompt=SYSTEM, checkpointer=MemorySaver())


def chat():
    config = {"configurable": {"thread_id": "demo"}}
    print("学习助手已启动，输入 quit 退出")
    print("试试这些问题：")
    print("  1) LangGraph 是什么？")
    print("  2) 帮我算 (128 * 46 + 37) / 3")
    print("  3) RAG 是怎么解决幻觉的？")
    print("  4) 我第一个问题问了什么？（测试记忆）\n")

    printed = 0  # 已打印的消息数，避免重复输出
    while True:
        q = input("你: ").strip()
        if q.lower() in {"quit", "exit"}:
            break
        if not q:
            continue
        # stream 让 Agent 的每一步思考/调用都实时可见
        for chunk in agent.stream({"messages": [("user", q)]}, config, stream_mode="values"):
            msgs = chunk["messages"]
            while printed < len(msgs):
                m = msgs[printed]
                printed += 1
                if m.type == "ai":
                    for tc in m.tool_calls:
                        print(f"  [调用工具] {tc['name']} 参数={tc['args']}")
                    if m.content:
                        print(f"助手: {m.content}\n")
                elif m.type == "tool":
                    print(f"  [工具返回] {m.content[:200]}")


if __name__ == "__main__":
    chat()
