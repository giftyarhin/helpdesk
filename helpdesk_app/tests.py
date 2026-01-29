from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Reply, SystemSettings


class MessageModelTest(TestCase):
    def setUp(self):
        self.message = Message.objects.create(
            sender_name="John Doe",
            sender_email="john@example.com",
            subject="Test Subject",
            message_body="This is a test message."
        )
    
    def test_message_creation(self):
        self.assertEqual(self.message.sender_name, "John Doe")
        self.assertEqual(self.message.status, "new")
    
    def test_message_string_representation(self):
        self.assertEqual(str(self.message), "John Doe - Test Subject")


class ReplyModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='testpass')
        self.message = Message.objects.create(
            sender_name="Jane Doe",
            sender_email="jane@example.com",
            subject="Question",
            message_body="I have a question."
        )
        self.reply = Reply.objects.create(
            message=self.message,
            admin=self.user,
            reply_body="Here is the answer."
        )
    
    def test_reply_creation(self):
        self.assertEqual(self.reply.message, self.message)
        self.assertEqual(self.reply.admin, self.user)


class SystemSettingsTest(TestCase):
    def test_settings_singleton(self):
        settings1 = SystemSettings.load()
        settings2 = SystemSettings.load()
        self.assertEqual(settings1.id, settings2.id)
