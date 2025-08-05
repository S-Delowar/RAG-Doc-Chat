
from typing import List, Optional, TypedDict


class AgentState(TypedDict, total=False):
    query: str
    session_id: int
    memory_context: str
    documents: List[str]
    rewritten_query: str
    next_tool: str
    web_search_results: str
    response: str