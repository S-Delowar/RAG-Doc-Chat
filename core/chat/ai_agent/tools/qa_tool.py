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
        You are smart to answer a query. Generate answer to the query with related context.
        User query:
        {state["rewritten_query"]}
        
        Context:
        {context}
        
        Previous chat history:
            {state["memory_context"]}
        """

        llm = get_llm()
        response = llm.invoke(prompt).content.strip()
        return {"response": response}

    return {"response": "No relevant documents found."}