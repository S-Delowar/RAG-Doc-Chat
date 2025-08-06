from core.chat.ai_agent.state import AgentState
from core.chat.ai_agent.utils.llm_utils import get_llm
from core.chat.ai_agent.vectorstore.chroma import get_chroma_vectorstore


def qa_tool(state:AgentState):
    vectorstore = get_chroma_vectorstore(f"session_{state['session_id']}")
    docs = vectorstore.similarity_search(state["rewritten_query"])
    
    if docs:
        context = "\n".join([doc.page_content for doc in docs])
        prompt = f"""You are smart to answer a query. Generate answer to the query with related context.
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