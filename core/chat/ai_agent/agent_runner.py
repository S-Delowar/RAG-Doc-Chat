from core.chat.ai_agent.graph_builder import build_agent_graph
from core.chat.ai_agent.memory.get_memory import get_memory_context

agent = build_agent_graph()

def run_agent(session, user_query):
    session_id = session.id
    memory_context = get_memory_context(session)
    
    result = agent.invoke({
        "query": user_query,
        "session_id": session_id,
        "memory_context": memory_context
    })
    
    return result.get("response", "Sorry, I couldn’t find an answer.")