
from typing import List, Optional, TypedDict


class AgentState(TypedDict, total=False):
    
    session_id: int
    query: str
    memory_context: str
    rewritten_query: str
    documents: List[str]
    next_tool: str
    web_search_results: str
    response: str