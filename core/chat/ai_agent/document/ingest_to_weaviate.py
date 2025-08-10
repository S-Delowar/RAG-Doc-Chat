import os
import tempfile
import boto3
from core.chat.ai_agent.document.loader import load_document
from core.chat.ai_agent.document.splitter import split_documents
from core.chat.ai_agent.vectorstore.weaviate import get_weaviate_client


def ingest_to_weaviate(session_id: str, file_field):
    """
    Loads a file, splits into chunks, and ingests into Weaviate.
    Each chunk gets stored with a session_id so it’s private to that user session.
    """
    client = get_weaviate_client()
    tmp_path = None 

    try:
        collection = client.collections.get("Document")

        # Download file from S3 or get local path
        tmp_path = _get_temp_file(file_field)

        print(f"tmp path: {tmp_path}")
        # Load and Split
        docs = load_document(tmp_path)
        chunks = split_documents(docs)

        # Prepare data
        data_objs = [
            {
                "session_id": session_id,
                "content": chunk.page_content,
                "source": file_field.url
            }
            for chunk in chunks
        ]

        collection.data.insert_many(data_objs)
        print(f"Ingested {len(data_objs)} chunks for session {session_id}")

    finally:
        client.close()
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
                print("Removed tmp path")
            except PermissionError:
                print(f"Warning: Could not delete temp file {tmp_path} (possibly still in use)")



def _get_temp_file(file_field):
    """
    Downloads the file to a temporary path if stored on S3,
    otherwise returns local path.
    Keeps file extension so loaders can detect file type.
    Works for both local and S3 storage.
    """
    storage = file_field.storage
    print(f"Storage location: {getattr(storage, 'location', None)}")
    print(f"Storage bucket name: {getattr(storage, 'bucket_name', None)}")

    # Get original file extension (e.g. ".pdf", ".docx")
    ext = os.path.splitext(file_field.name)[1].lower()

    # If using S3Boto3Storage
    if hasattr(storage, 'bucket_name'):
        s3 = boto3.client("s3")
        bucket_name = storage.bucket_name
        # Build correct key with storage location if present
        key = f"{storage.location}/{file_field.name}" if storage.location else file_field.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
            s3.download_fileobj(bucket_name, key, tmp_file)
            return tmp_file.name

    # Local storage
    return file_field.path