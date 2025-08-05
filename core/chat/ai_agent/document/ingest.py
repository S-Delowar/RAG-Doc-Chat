from core.chat.ai_agent.document.loader import load_document
from core.chat.ai_agent.document.splitter import split_documents
from core.chat.ai_agent.vectorstore.chroma import get_chroma_vectorstore


def ingest_to_chroma(session_id, file_path):
    
    docs = load_document(file_path)
    chunks = split_documents(docs)
    
    collection_name = f"session_{session_id}"
    vectorstore = get_chroma_vectorstore(collection_name)
    
    vectorstore.add_documents(chunks)
    
    
    

if __name__ == "__main__":
    file_path = "requirements.txt"
    ingest_to_chroma("dhdhggggggg232", file_path)