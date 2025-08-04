import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from core.chat.models.chat_message import ChatMessage
from core.chat.models.chat_session import ChatSession
from core.chat.models.document import Document


User = get_user_model()

# -------------------------
# Fixtures
# -------------------------

@pytest.fixture
def user(db):
    return User.objects.create_user(username='tester', email="testuser@mail.com", password='testpass')


@pytest.fixture
def session(user):
    return ChatSession.objects.create(user=user, title='My Chat')


# -------------------------
# Session Tests
# -------------------------

def test_create_session(session, user):
    assert session.id is not None
    assert session.user == user
    assert str(session) == 'My Chat'

def test_deleting_session_deletes_related(session):
    Document.objects.create(session=session, file=SimpleUploadedFile("a.pdf", b"123"))
    ChatMessage.objects.create(session=session, sender='user', content='hi')
    assert Document.objects.count() == 1
    assert ChatMessage.objects.count() == 1
    session.delete()
    assert Document.objects.count() == 0
    assert ChatMessage.objects.count() == 0

# -------------------------
# Document Tests
# -------------------------

def test_document_upload(session):
    doc = Document.objects.create(
        session=session,
        file=SimpleUploadedFile("test.txt", b"abc")
    )
    assert doc.id
    assert doc.file.name.startswith('documents/')
    assert doc.file.name.endswith('.txt')


def test_multiple_documents_for_session(session):
    for i in range(2):
        Document.objects.create(
            session=session,
            file=SimpleUploadedFile(f"file{i}.txt", b"x")
        )
    assert session.documents.count() == 2


# -------------------------
# Message Tests
# -------------------------

def test_create_user_and_bot_messages(session):
    user_msg = ChatMessage.objects.create(session=session, sender='user', content='Hello')
    bot_msg = ChatMessage.objects.create(session=session, sender='bot', content='Hi there')

    assert user_msg.sender == 'user'
    assert bot_msg.sender == 'bot'
    assert session.chat_messages.count() == 2


def test_message_ordering(session):
    m1 = ChatMessage.objects.create(session=session, sender='user', content='first')
    m2 = ChatMessage.objects.create(session=session, sender='bot', content='second')
    messages = list(session.chat_messages.all())

    assert messages[0].timestamp <= messages[1].timestamp


def test_message_str_output(session):
    msg = ChatMessage.objects.create(session=session, sender='user', content='A long message here')
    assert '[user]' in str(msg)
