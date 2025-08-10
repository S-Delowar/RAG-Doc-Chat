from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from core.chat.ai_agent.document.ingest_to_weaviate import ingest_to_weaviate
from core.chat.models.document import Document


@receiver(pre_delete, sender=Document)
def delete_document_file_from_s3(sender, instance, **kwargs):
    """
    Deletes the associated file from S3 before the Document instance is deleted.
    """
    if instance.file:
        instance.file.delete(save=False)
         

@receiver(post_save, sender=Document)
def handle_ingest_to_weaviate(sender, instance, created, **kwargs):
    """
    Ingest document into Weaviate after it's uploaded and saved.
    """
    if created and instance.file:
        try:
            session_id = str(instance.session.id)
            ingest_to_weaviate(session_id, instance.file)
        except Exception as e:
            print(f"Weaviate ingestion failed: {e}")
