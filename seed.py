import os
import time
import datetime

"""
This function will seed the database
with some users tools sheds, ect
for testing and what not
"""
def seed():
    d = datetime.datetime.now()
    d.replace(year = d.year - 21)
    community = Community(zipcode=12345,name="Hollywood")
    community.save()
    shed1 = Shed(community=community, name="Home", shed_address="Home", is_home=True)
    shed1.save()
    community_wall = communityWall(wall_name=str(community.zipcode), community=community)
    community_wall.save()
    deleted = communityWall(wall_name="deleted", community=community, is_deleted=True)
    deleted.save()

    community2 = Community(zipcode=54321,name="Park Ave")
    community2.save()
    shed2 = Shed(community=community2, name="Home", shed_address="Home", is_home=True)
    shed2.save()
    community_wall2 = communityWall(wall_name=str(community2.zipcode), community=community2)
    community_wall2.save()
    deleted2 = communityWall(wall_name="deleted", community=community2, is_deleted=True)
    deleted2.save()
    
    user = ourUser(age=d, username="MC", zipcode=12345, password="pbkdf2_sha256$12000$FeEvdT08GvsR$4yWK3pnJ1De4szo4V3ZSqoJOnSR0RPu3DtadIMT/VUQ=",community=community, address="12 Main St.")
    user.save()
    user2 = ourUser(age=d, username="Doctor_Who", zipcode=12345, password="pbkdf2_sha256$12000$FeEvdT08GvsR$4yWK3pnJ1De4szo4V3ZSqoJOnSR0RPu3DtadIMT/VUQ=",community=community, address="13 Main St.")
    user2.save()
    user3 = ourUser(age=d, username="Sherlock", zipcode=12345, password="pbkdf2_sha256$12000$FeEvdT08GvsR$4yWK3pnJ1De4szo4V3ZSqoJOnSR0RPu3DtadIMT/VUQ=",community=community, address="26 Baker St")
    user3.save()
    user4 = ourUser(age=d, username="John_Stamos", zipcode=12345, password="pbkdf2_sha256$12000$FeEvdT08GvsR$4yWK3pnJ1De4szo4V3ZSqoJOnSR0RPu3DtadIMT/VUQ=",community=community, address="Krutz's Neighbor")
    user4.save()
    user5 = ourUser(age=d, username="Elvis", zipcode=12345, password="pbkdf2_sha256$12000$FeEvdT08GvsR$4yWK3pnJ1De4szo4V3ZSqoJOnSR0RPu3DtadIMT/VUQ=",community=community, address="Memphis Lane")
    user5.save()

    user6 = ourUser(age=d, username="mlutz", zipcode=54321, password="pbkdf2_sha256$12000$FeEvdT08GvsR$4yWK3pnJ1De4szo4V3ZSqoJOnSR0RPu3DtadIMT/VUQ=",community=community2, address="123 Park Ave")
    user6.save()
    user7 = ourUser(age=d, username="dkrutz", zipcode=54321, password="pbkdf2_sha256$12000$FeEvdT08GvsR$4yWK3pnJ1De4szo4V3ZSqoJOnSR0RPu3DtadIMT/VUQ=",community=community2, address="1231 Park Ave")
    user7.save()
    user8 = ourUser(age=d, username="bgates", zipcode=54321, password="pbkdf2_sha256$12000$FeEvdT08GvsR$4yWK3pnJ1De4szo4V3ZSqoJOnSR0RPu3DtadIMT/VUQ=",community=community2, address="122 Park Ave")
    user8.save()
    user9 = ourUser(age=d, username="sjobs", zipcode=54321, password="pbkdf2_sha256$12000$FeEvdT08GvsR$4yWK3pnJ1De4szo4V3ZSqoJOnSR0RPu3DtadIMT/VUQ=",community=community2, address="641 Park Ave")
    user9.save()



    community.admin = user
    community.save()
    community2.admin = user7
    community2.save()

    shed3 = Shed(admin=user,name="Superstars",community=community,shed_address="56 Main St.",is_home=False)
    shed3.save()

    tool = Tool(name="Hammer",owner=user,borrower=None,shed=shed1,description="This hammer is so great you can't touch this", is_active=True, community=community, pickup_arrangements="Come to my house")
    tool.save()
    tool2 = Tool(name="Sonic Screwdriver",owner=user2,borrower=None,shed=shed3,description="It makes cool sounds.", is_active=True, community=community, pickup_arrangements="")
    tool2.save()
    tool3 = Tool(name="Wig made of my own hair",owner=user4,borrower=None,shed=shed3,description="For when you need to look fantastic", is_active=True, community=community, pickup_arrangements="")
    tool3.save()
    tool4 = Tool(name="Hammer",owner=user2,borrower=None,shed=shed3,description="It has my username on the handle", is_active=True, community=community, pickup_arrangements="")
    tool4.save()
    tool5 = Tool(name="Gibson J-200",owner=user5,borrower=None,shed=shed3,description="Played it a few times.", is_active=True, community=community, pickup_arrangements="")
    tool5.save()
    tool8 = Tool(name="Pipe",owner=user,borrower=None,shed=shed3,description="This is not a pipe", is_active=True, community=community, pickup_arrangements="")
    tool8.save()


    tool5 = Tool(name="iPod Classic",owner=user9,borrower=None,shed=shed2,description="A great old music player", is_active=True, community=community2, pickup_arrangements="Come on over and knock on my door")
    tool5.save()
    tool6 = Tool(name="iPod Classic",owner=user8,borrower=None,shed=shed2,description="An adequate hammer when the need arises", is_active=True, community=community2, pickup_arrangements="Come on over and knock on my door")
    tool6.save()
    tool7 = Tool(name="Elements of Reusable Object-Oriented Software",owner=user7,borrower=None,shed=shed2,description="My favorite book. Borrow it!", is_active=True, community=community2, pickup_arrangements="Come to my door with a coffee")
    tool7.save()

    res = Reservation(approved=True,tool=tool,community=community,borrow_request_date=datetime.datetime.now(),return_date=datetime.datetime.now() + datetime.timedelta(days=1),borrower=user4,owner=user,is_active=False)
    res.save()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ToolShare.settings")
    from toolshareapp.models import *
    from userMessaging.models import *
    from userManagement.models import *
    from messageBoard.models import *
    from django.contrib.auth.models import User
    from django.shortcuts import get_object_or_404
    seed()