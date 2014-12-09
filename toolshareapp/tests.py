from django.test import TestCase

from toolshareapp.views import search_objects
from toolshareapp.models import Tool, Shed, Community, Reservation
from userManagement.models import ourUser, feedBack
from messageBoard.models import communityWall, Post
from datetime import datetime

from django.db import models
from django.http import HttpRequest

# Create your tests here.

"""
Test Class Format:

class NameOfClassTestCase(TestCase):
    def setUp(self):
        Set up required attributes for testing

    def test_ThingToTest(self):
        Set up test specific attributes
        self.assertEqual(method,"expected result")

"""



from testfactory import TestFactory

class CommunityTestCase(TestCase):
    def setUp(self):
        TestFactory.setUpAll()
        
    def test_list_available(self):
        # self.assertEqual()
        pass

# Create your tests here.
class ToolTestCase(TestCase):
    def setUp(self):
        TestFactory.setUpAll()

    def test_return_tool(self):
        user1 = ourUser.objects.get(username = 'TestUser1')
        user2 = ourUser.objects.get(username = 'TestUser2')
        tool = Tool.objects.get(description = 'This is a hammer.')

        # Uncomment code once this works
        # (a user is being set to False for some reason)
        """
        tool.return_tool()
        self.assertEqual(tool.borrower, None)
        self.assertEqual(tool.owner.username, 'TestUser1')
        """

class ShedTestCase(TestCase):

    def setUp(self):
        TestFactory.setUpAll()

    def test_create(self):
        shed = Shed.objects.get(name='First Shed')
        user = ourUser.objects.get(username='TestUser1')
        shed.create(user)
        self.assertEqual(user, shed.admin)
        self.assertEqual(user.community, shed.community)
        self.assertEqual(shed.is_home, False)

    def test_manage_tool(self):
        shed = Shed.objects.get(name = 'First Shed')
        tool1 = Tool.objects.get(name = 'Hammer')
        # assert equal
    def test_remove_tool(self):
        shed = Shed.objects.get(name = 'First Shed')
        tool1 = Tool.objects.get(name = 'Hammer')
        # assert equal
    def test_list_available(self):
        # self.assertEqual()
        pass

class ReservationTestCase(TestCase):

    def setUp(self):
        TestFactory.setUpAll()

    def test_validate_borrow(self):
        pass

    def test_validate_return(self):
        pass

    def test_validate_availability(self):
        pass

    def test_send_deny(self):
        pass

    def test___str__(self):
        user = ourUser.objects.get(username='TestUser1')
        reservation = Reservation.objects.get(borrow_request_date = TestFactory.def_date)
        self.assertEqual(reservation.borrower,user)
        res_test = Reservation.objects.get(borrower = reservation.borrower)
        username1 = user.username
        username2 = ourUser.objects.get(username='TestUser2').username
        reqDate = str(reservation.borrow_request_date)
        string = username1 + "_" + username2 + "_" + reqDate
        self.assertEqual(string, reservation.__str__())

class UserTestCase(TestCase):
    def setUp(self):
        # create user
        pass
    def test_add_tool(self):
        # self.assertEqual()
        pass
    def test_remove_tool(self):
        # self.assertEqual()
        pass
    def test_change_address(self):
        # self.assertEqual()
        pass
    def test_make_reservation(self):
        # self.assertEqual()
        pass
    def test_create_shed(self):
        # self.assertEqual()
        pass


class ReputationTestCase(TestCase):
    def setUp(self):
        # create reputation
        pass
    def test_vote(self):
        # self.assertEqual()
        pass
    def test_update(self):
        # self.assertEqual()
        pass


class ReservationControllerTestCase(TestCase):
    def setUp(self):
        # create reservation controller
        pass
    def test_check_validity(self):
        # self.assertEqual()
        pass
    def test_display_tools(self):
        # self.assertEqual()
        pass
    def test_check_availability(self):
        # self.assertEqual()
        pass
    def test_get_rep(self):
        # self.assertEqual()
        pass


class StatsControllerTestCase(TestCase):
    def setUp(self):
        # create stats controller
        pass
    def test_most_active_lenders(self):
        # self.assertEqual()
        pass
    def test_most_active_borrowers(self):
        # self.assertEqual()
        pass
    def test_most_used_tools(self):
        # self.assertEqual()
        pass
    def test_most_recent_used_tools(self):
        # self.assertEqual()
        pass
    def test_display_stats(self):
        # self.assertEqual()
        pass


class AdminTestCase(TestCase):
    def setUp(self):
        # create admin
        pass
    def test_ban_user(self):
        # self.assertEqual()
        pass
    def test_promote_user(self):
        # self.assertEqual()
        pass
    def test_create_community(self):
        # self.assertEqual()
        pass
    def test_remove_user(self):
        # self.assertEqual()
        pass


class CommunityWallTestCase(TestCase):
    def setUp(self):
        # create community
        community = Community(
            zipcode = 14626,
            name = 'First Community')
        community.save()
        # create community wall
        community_wall = communityWall(
            wall_name = 'Test Wall Name',
            community = community)
    def test_delete(self):
        # self.assertEqual()
        pass
    def test_delete_post(self):
        # self.assertEqual()
        pass
    def test_edit(self):
        # self.assertEqual()
        pass

class HTTPRequestSearch(HttpRequest):
    user = models.ForeignKey('userManagement.ourUser',null=True, blank=True, related_name='comm_admin')
    
class SearchObjectsTestCase(TestCase):
    def setUp(self):
        pass
    
    def assertContains(self, l_string, r_string):
        if l_string not in r_string:
            raise AssertionError("Assertion failed. Left string not found in right string.")

    def test_search_objects(self):
        #community = TestFactory.createCommunity()
        #user1 = TestFactory.createUserOne(community)
        #user2 = TestFactory.createUserTwo(community)
        #shed = TestFactory.createShed(user1, community)
        tool = TestFactory.createTool()

        # Create a new request
        request = HTTPRequestSearch()

        # A user searches for "Hamm". Hammer should come up.
        request.user = tool.owner
        request.GET['q'] = "Hamm"

        # Search and make sure the response has a "Hammer" result.
        resp = search_objects(request)
        self.assertContains("Hammer", resp.content.decode("utf-8"))

"""

class PostTestCase(TestCase):
    def setUp(self):
        # create community
        community = Community(
            zipcode = 14626,
            name = 'First Community')
        community.save()
        # create user
        user = ourUser(
            community = community,
            reputation = 2,
            zipcode = 14626,
            address = '3 Circle Street',
            username = 'TestUser',
            password = 'password')
        user.save()
        # create community wall
        community_wall = communityWall(
            wall_name = 'Test Wall Name',
            community = community)
        community_wall.save()
        # create post
        post = Post(
            post_title = 'Test Post',
            timestamp_post = datetime.now(),
            poster = user,
            wall = community_wall,
            content = 'This is a test post.')
        post.save()
    def test_post(self):
        # self.assertEqual()
        pass
    def test_delete(self):
        post = Post.objects.get(post_title = 'Test Post')
        community_wall = communityWall.objects.get(wall_name = 'Test Wall Name')
        self.assertEqual(post.wall, community_wall)
        post.delete()
        self.assertEqual(post.wall, None)
        # self.assertEqual()
        pass


class DashboardControllerTestCase(TestCase):
    def setUp(self):
        # create dashboard controller
        pass
    def test_display(self):
        # self.assertEqual()
        pass
    def test_getPosts(self):
        # self.assertEqual()
        pass


class MailBoxTestCase(TestCase):
    def setUp(self):
        # create mail box
        pass
    def test_delete_message(self):
        # self.assertEqual()
        pass
    def test_delete(self):
        # self.assertEqual()
        pass


class MessageControllerTestCase(TestCase):
    def setUp(self):
        # create message controller
        pass
    def test_display_mail(self):
        # self.assertEqual()
        pass
    def test_get_messages(self):
        # self.assertEqual()
        pass
    def test_send(self):
        # self.assertEqual()
        pass


class MessageTestCase(TestCase):
    def setUp(self):
        # create message
        pass
    def test_delete(self):
        # self.assertEqual()
        pass




class toolshareappTestClass(TestCase):
    def setUp(self):

        #tool attributes
        name = "Hammer"
        test_owner_id = 2
        test_borrower_id = 1
        test_description = "This is a test hammer."
        test_is_active = True
        test_shed = 1

        #commence obnoxious create function length
        self.tool = toolshareapp.objects.create(name=name, owner_id=test_owner_id,
                                                borrower_id=test_borrower_id,
                                                description=test_description,
                                                is_active=test_is_active,
                                                shed=test_shed)
"""
