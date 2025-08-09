import os
import weaviate
from weaviate.classes.config import Property, DataType
import weaviate.classes.config as wvc
from weaviate.auth import AuthApiKey

from dotenv import load_dotenv

load_dotenv()

WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

def get_weaviate_client():
    """
    Connect to Weaviate Cloud and ensure the 'Document' schema exists.
    Returns a connected client.
    """
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=WEAVIATE_URL,
        auth_credentials=AuthApiKey(WEAVIATE_API_KEY),
        headers={"X-Openai-Api-Key": os.getenv("OPENAI_API_KEY")},
    )

    # Create schema
    existing_collections = client.collections.list_all()
    if "Document" not in existing_collections:
        print("Creating 'Document' collection in Weaviate...")
        client.collections.create(
            name="Document",
            vector_config=wvc.Configure.Vectors.text2vec_openai(),
            properties=[
                Property(name="session_id", 
                        data_type=DataType.TEXT,
                        description="Session ID"),
                Property(name="content",
                        data_type=DataType.TEXT,
                        description="Document chunk text"),
                Property(name="source",
                        data_type=DataType.TEXT,
                        description="File name or source"),
            ]
        )
        print("Schema created successfully.")
        
    return client