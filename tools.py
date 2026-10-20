"""Agent 的工具箱。

每个 @tool 装饰的函数就是一个工具。模型通过 docstring（中文注释）
理解这个工具是干什么的、什么时候该用，所以注释一定要写清楚。
"""
from pathlib import Path

from langchain_core.tools import tool

KB_DIR = Path(__file__).parent / "kb"


@tool
def calculator(expression: str) -> str:
    """计算数学表达式。输入为合法算式，如 "12 * (3 + 4) / 5"。"""
    allowed = set("0123456789+-*/().% ")
    if not set(expression) <= allowed:
        return "表达式含非法字符，只支持数字、+ - * / % 和括号"
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"计算出错：{e}"


def _score(query: str, text: str) -> int:
    """用「二字组重合度」给文档打分：查询越相关，得分越高。
    这是 RAG 检索的最简实现；真实 RAG 用 Embedding 向量相似度，思想相同。"""
    q = query.replace(" ", "")
    return sum(text.count(q[i : i + 2]) for i in range(len(q) - 1))


@tool
def kb_search(query: str) -> str:
    """在本地知识库中检索 Agent 相关概念的解释。
    当用户询问 LangGraph、ReAct、RAG、记忆、工具调用等概念时使用。"""
    best_text, best_score = "", 0
    for f in KB_DIR.glob("*.md"):
        text = f.read_text(encoding="utf-8")
        s = _score(query, text)
        if s > best_score:
            best_text, best_score = text, s
    if not best_text or best_score == 0:
        return "知识库中没有找到相关内容"
    return best_text[:600]
