import os
from tavily import TavilyClient
from dotenv import load_dotenv

from core.chat.ai_agent.state import AgentState
from core.chat.ai_agent.utils.llm_utils import get_llm

load_dotenv()



def web_search_tool(state:AgentState):
    query = state["rewritten_query"]
    memory = state["memory_context"]
    
    llm = get_llm()
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    
    results = tavily_client.search(query=query, max_results=2)
    
    # Exract content from tavily search
    web_content = "\n".join([
        f"{res['title']}: {res['content']}" for res in results.get("results", [])
    ])
    
    if not web_content.strip():
        return {"response": "Sorry, I couldn't find any relevant information online."}
    
    prompt = f"""
        You are a helpful assistant. 
        
        Here is the user query:
        {query}
        
        Here is some relevant web search result content:
        {web_content}
        
        Memory from the conversation:
        {memory}
        
        Now generate a clear, concise and helpful answer.
    """
    
    response = llm.invoke(prompt).content.strip()
    
    return {"response": response}