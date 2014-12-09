from django.test import TestCase
from testfactory import TestFactory
from toolshareapp.models import Reservation, Community, Tool
from userManagement.models import feedBack, ourUser

# Create your tests here.
class FeedBackTestCase(TestCase):
    def setUp(self):
        testfactory = TestFactory()
        testfactory.setUpAll()

    def test_post(self):
        reservation = Reservation.objects.get(borrow_request_date = TestFactory.def_date)
        self.assertEqual(reservation.feed_back_given, False)
        feedback = feedBack.objects.get(comment = "Test Comment")
        feedback.post(reservation)
        self.assertEqual(reservation.feed_back_given, True)
        self.assertEqual(reservation.owner, feedback.rater)
        self.assertEqual(reservation.borrower, feedback.user)

class OurUserTestCase(TestCase):
    
    testfactory = TestFactory()
    
    def setUp(self):
        OurUserTestCase.testfactory.setUpAll()

    def test___init__(self):
        pass

    def test_join(self):
        user = ourUser.objects.get(username = "TestUser1")
        community = OurUserTestCase.testfactory.createSecondCommunity(10001, 'NYC Community')
        tools = Tool.objects.filter(owner = user)
        reserved_tools = []
        for tool in tools:
            if tool.borrower is not None:
                reserved_tools.append(tool)
        borrowed_res = Reservation.objects.filter(borrower = user)
        owned_res = Reservation.objects.filter(owner = user)
        user.join(community, tools, owned_res, reserved_tools, borrowed_res)
        self.assertEqual(user.community.name, "NYC Community")
        for tool in tools:
            self.assertEqual(tool.borrower, None)
        
