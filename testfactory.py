from toolshareapp.models import Tool, Shed, Community, Reservation
from userManagement.models import ourUser, feedBack
from userMessaging.models import Message
from messageBoard.models import communityWall, Post
import datetime

"""
Has methods for creating objects to use for tests.
Uses a factory pattern.
"""
class TestFactory:
    
    """
    create a default datetime to be used by
    this class and many classes that import TestFactory.
    Since time is continuously changing, a current time has to
    be saved and referenced.
    """
    def_date = datetime.datetime.now()

    @staticmethod
    def createCommunity():
        # create community
        community = Community(
            zipcode = 14626,
            name = 'First Community')
        community.save()
        return community

    @staticmethod
    def createSecondCommunity(zipcode, name):
        # create community
        community = Community(
            zipcode = zipcode,
            name = name)
        community.save()
        return community

    @staticmethod
    def createTwoUsers(community=None):
        # creates two users
        if community is None:
            community = createCommunity()
            
        createUserOne(community)
        createUserTwo(community)

    @staticmethod
    def createUserOne(community=None):
        # create first user
        if community is None:
            community = createCommunity()
        user1 = ourUser(
            community = community,
            age = datetime.datetime(1992, 7, 31),
            zipcode = 14626,
            address = '3 Circle Street',
            username = 'TestUser1',
            password = 'password')
        user1.save()
        return user1

    @staticmethod
    def createUserTwo(community=None):
        # create second user
        if community is None:
            community = createCommunity()
        user2 = ourUser(
            community = community,
            zipcode = 14626,
            age = datetime.datetime(1993, 1, 4),
            address = '4 Circle Street',
            username = 'TestUser2',
            password = 'password')
        user2.save()
        return user2

    @staticmethod
    def createShed(user1=None, community=None):
        if community is None:
            community = createCommunity()
        if user1 is None:
            user1 = createUserOne(community)
        shed = Shed(
            admin = user1,
            name = 'First Shed',
            community = community,
            shed_address = '4 Circle Street',
            is_home = False)
        shed.save()
        return shed

    @staticmethod
    def createTool(user1=None, user2=None, shed=None, community=None):
        # create tool
        if community is None:
            community = TestFactory.createCommunity()
        if user1 is None:
            user1 = TestFactory.createUserOne(community)
        if user2 is None:
            user2 = TestFactory.createUserTwo(community)
        if shed is None:
            shed = TestFactory.createShed(user1, community)
        tool = Tool(
            name = 'Hammer',
            owner = user1,
            borrower = user2,
            shed = shed,
            description = 'This is a hammer.',
            is_active = True,
            community = community)
        tool.save()
        return tool

    @staticmethod
    def createReservation(tool=None, community=None, user1=None, user2=None):
        # create reservation
        if community is None:
            community = createCommunity()
        if user1 is None:
            user1 = createUserOne(community)
        if user2 is None:
            user2 = createUserTwo(community)
        if tool is None:
            tool = createTool(user1, user2, community)
        reservation = Reservation(
            tool = tool,
            community = community,
            borrow_request_date = TestFactory.def_date,
            return_date = TestFactory.def_date + datetime.timedelta(days=2),
            borrower = user1,
            owner = user2,
            is_active = True)
        reservation.save()
        return reservation

    @staticmethod
    def createMessage(user1=None, user2=None, reservation=None):
        # create message
        if user1 is None:
            user1 = createUserOne()
        if user2 is None:
            user2 = createUserTwo()
        message = Message(
            date_sent = datetime.datetime.now()-datetime.timedelta(days=1),
            subject = "Test Message",
            contents = "This is a test message",
            sender = user1,
            receiver = user2)
        message.save()
        return message

    @staticmethod
    def createStatistics(community=None):
        if community is None:
            community = createCommunity()
        statistics = Statistics(
            community = community)
        statistics.save()
        
    @staticmethod
    def createFeedBack(user1=None, user2=None, reputation=4, comment="Test Comment", is_active=True):
        #create feedback
        if user1 is None:
            user1 = createUserOne()
        if user2 is None:
            user2 = createUserTwo()
        feedback = feedBack(
            user = user1,
            rater = user2,
            reputation = reputation,
            comment = comment,
            is_active = is_active)
        feedback.save()
    
    @staticmethod
    def setUpAll():
        community = TestFactory.createCommunity()
        user1 = TestFactory.createUserOne(community)
        user2 = TestFactory.createUserTwo(community)
        shed = TestFactory.createShed(user1, community)
        tool = TestFactory.createTool(user1, user2, shed, community)
        reservation = TestFactory.createReservation(tool, community, user1, user2)
        message = TestFactory.createMessage(user1, user2, reservation)
        feedback = TestFactory.createFeedBack(user1, user2)
