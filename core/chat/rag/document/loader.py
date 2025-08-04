from langchain_community.document_loaders import PyMuPDFLoader, TextLoader, UnstructuredWordDocumentLoader

def load_document(file_path: str):
    if file_path.endswith(".pdf"):
        return PyMuPDFLoader(file_path).load()
    elif file_path.endswith(".txt"):
        return TextLoader(file_path).load()
    elif file_path.endswith(".docx"):
        return UnstructuredWordDocumentLoader(file_path).load()
    else:
        raise ValueError("Unsupported file type")
