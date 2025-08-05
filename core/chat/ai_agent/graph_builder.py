from langgraph.graph import StateGraph

from core.chat.ai_agent.state import AgentState
from core.chat.ai_agent.tools.direct_tool import direct_tool
from core.chat.ai_agent.tools.qa_tool import qa_tool
from core.chat.ai_agent.tools.query_rewriter_tool import rewrite_query_node
from core.chat.ai_agent.tools.router import router_node
from core.chat.ai_agent.tools.web_tool import web_search_tool


def build_agent_graph():
    graph_builder = StateGraph(AgentState)
    
    graph_builder.add_node("rewrite_query", rewrite_query_node)
    graph_builder.add_node("router", router_node)
    graph_builder.add_node("qa_tool", qa_tool)
    graph_builder.add_node("web_tool", web_search_tool)
    graph_builder.add_node("direct_tool", direct_tool)
    
    graph_builder.set_entry_point("rewrite_query")
    graph_builder.add_edge("rewrite_query", "router")
    graph_builder.add_conditional_edges("router", {
        "qa_tool": qa_tool,
        "direct_tool": direct_tool,
        "web_tool": web_search_tool,
    })
    
    return graph_builder.compile()