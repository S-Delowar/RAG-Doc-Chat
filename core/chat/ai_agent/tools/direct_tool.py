from core.chat.ai_agent.state import AgentState
from core.chat.ai_agent.utils.llm_utils import get_llm


def direct_tool(state: AgentState):
    prompt = f"Chat Memory:\n{state['memory_context']}\nUser: {state['rewritten_query']}"
    llm = get_llm()
    response = llm.invoke(prompt).content.strip()
    return {"response": response}