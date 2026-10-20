# LangGraph 入门

LangGraph 是 LangChain 团队开发的 Agent 编排框架，用「图（Graph）」来描述 Agent 的执行流程：
节点（Node）是每一步操作（如调用模型、执行工具），边（Edge）定义步骤之间的跳转关系。

核心概念：
- State：在图中流转的状态对象，通常包含消息列表。
- Node：处理 State 并返回更新的函数。
- Edge：决定下一个执行哪个节点，支持条件分支。
- Checkpointer：把 State 持久化，实现记忆与断点续跑。

对初学者最常用的入口是 langchain.agents.create_agent，
一行代码就能得到带工具调用循环的 ReAct Agent，不用自己画图。
