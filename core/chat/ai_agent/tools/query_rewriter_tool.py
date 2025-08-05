from core.chat.ai_agent.state import AgentState
from core.chat.ai_agent.utils.llm_utils import get_llm

llm = get_llm()


def rewrite_query_node(state:AgentState):
    prompt = f"Rewrite this query for clarity: {state['query']}"
    rewritten = llm.invoke(prompt)
    state["rewritten_query"] = rewritten.content.strip()
    
    return state