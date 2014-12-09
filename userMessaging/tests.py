from django.test import TestCase
from userMessaging.models import Message
from userManagement.models import ourUser
from testfactory import TestFactory
from datetime import datetime

# Create your tests here.
class MessageTestCase(TestCase):
    def setUp(self):
        TestFactory.setUpAll()

    def test_create(self):
        message = Message.objects.get(subject = 'Test Message')
        time = message.date_sent
        user = ourUser.objects.get(username = 'TestUser1')
        message.create(user)
        self.assertEqual(message.sender,user)
        self.assertGreater(message.date_sent, time)

    def test_delete_message(self):
        message = Message.objects.get(subject = 'Test Message')
        message.delete_message()
        self.assertEqual(message.receiver, None)
