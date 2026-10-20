# learnagent

我的第一个 LangGraph Agent 项目：一个带工具调用和记忆的命令行学习助手。

## 功能

- **ReAct 循环**：基于 `langchain.agents.create_agent`，模型自主完成「思考 → 调用工具 → 观察 → 再思考」
- **工具调用**：计算器 + 本地知识库检索（mini-RAG，关键词重合度打分）
- **对话记忆**：`MemorySaver` checkpointer，同一线程内记住上下文
- **过程可见**：流式打印每一步工具调用与返回，方便观察 Agent 的决策过程

## 结构

```text
learnagent/
├── agent.py           # 主程序：LLM + 工具 + 记忆 + CLI
├── tools.py           # 工具箱：calculator / kb_search
├── kb/                # 本地知识库（Agent 概念文档）
├── requirements.txt
└── .env.example       # API Key 模板
```

## 运行

```bash
pip install -r requirements.txt
cp .env.example .env   # 填入你的 DeepSeek API Key
python agent.py
```

模型使用 DeepSeek（OpenAI 兼容接口），换其他模型只需修改 `agent.py` 中的 `model` 与 `base_url`。
