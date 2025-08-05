from core.chat.ai_agent.state import AgentState
from core.chat.ai_agent.utils.llm_utils import get_llm


llm = get_llm()

def router_node(state:AgentState):
    query = state["rewritten_query"]
    memory = state["memory_context"]
    
    prompt = f"""
        You are a smart tool router.
        
        User query: "{query}"
        
        Based on the query, select the best tool to use.
        Available tools:
        - direct_tool: Answer without retrieval if question is casual or simple.
        - qa_tool: Use if answering requires context from uploaded document.
        - web_tool: Use if the question can't be answered from the document.
        
        Return only one of: direct_tool, qa_tool, web_tool.
    """
    
    tool = llm.invoke(prompt).content.strip().lower()
    
    if tool not in {"direct_tool", "qa_tool", "web_tool"}:
        tool = "direct_tool"

    return {"next_tool": tool}



def route_decision(state: AgentState):
    return state["next_tool"]


        # - summary_tool: Use if the user asks to summarize a document or chat.
#