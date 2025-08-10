from weaviate.classes.query import Filter
from core.chat.ai_agent.state import AgentState
from core.chat.ai_agent.utils.llm_utils import get_llm
from core.chat.ai_agent.vectorstore.weaviate import get_weaviate_client


def qa_tool(state: AgentState):
    """
    Performs a RAG query for a given session_id, using only that user's uploaded docs.
    """
    client = get_weaviate_client()
    collection = client.collections.get("Document")

    # Filter by session_id so users don't see each other's docs
    results = collection.query.near_text(
        query=state["rewritten_query"],
        filters=Filter.by_property("session_id").equal(state["session_id"]),
        limit=5
    )
    
    client.close()

    if results.objects:
        context = "\n".join([obj.properties["content"] for obj in results.objects])
        prompt = f"""
        You are a helpful AI assistant. 
        
        Please answer the user query clearly and directly, using only the provided context.

        Important:
        - Do NOT add any prefixes, labels, greetings, or introductory words such as "AI:", "Answer:", "Response:", or anything similar.
        - Do NOT say "Here is the answer", "AI says", or any other framing.
        - ONLY provide the plain text answer, nothing else.
            
        User query:
        {state["rewritten_query"]}
        
        Context:
        {context}
        
        Previous chat history:
            {state["memory_context"]}
        """

        llm = get_llm()
        response_text = llm.invoke(prompt).content.strip()
        
        for prefix in ("Answer:", "Response:", "AI:"):
            if response_text.lower().startswith(prefix.lower()):
                response_text = response_text[len(prefix):].strip()
                
        return {"response": response_text}
