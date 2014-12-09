from django.db import models
import datetime
from ToolShare.validators import validate_txt_feild

"""
#Community Wall class
"""

#class for a community wall
#each wall has lots of posts on it
#each wall has a displayed name and a community
#it is attached to
class communityWall(models.Model):
    #name of the community wall
    wall_name = models.CharField(max_length=50)
    #the community the wall is tied to
    community = models.ForeignKey('toolshareapp.Community')
    is_deleted = models.BooleanField(default=False)

    #gives the name of the wall
    def __str__(self):
        return self.wall_name

    #deletes the wall
    def delete_wall(self, t):
        t.community = None
        t.save()



"""
#Post class
"""

#class for a post to the community wall
#each post has a title, time it was posted, person posting it,
#the wall it is posting to, and the content of the post
class Post(models.Model):
    timestamp_post = models.DateTimeField()
    #added poster as related name, one person has many posts
    poster = models.ForeignKey('userManagement.ourUser', related_name='poster')
    #ties the posts to the walls
    wall = models.ForeignKey('communityWall', null=True)
    #the main written portion of the community post
    content = models.TextField(max_length=1000,validators=[validate_txt_feild])


#gives the name of the post
    def __str__(self):
        return self.content

# #makes post to community wall by assigning wall id to the post
    def post_handler(self, t, user):
        args = {}
        self.poster = user
        self.timestamp_post = datetime.datetime.now()
        self.wall = t
        self.save()
        args['post'] = self
        args['post_id'] = self.id
        args['user'] = user
        return args

    def delete(self):

        deleted = list(communityWall.objects.filter(wall_name="deleted").filter(community=self.poster.community))
        self.wall = deleted[0]
        self.save()


#edit the info for desired post
    def edit(self, t, **kwargs):
        for name, value in kwargs.items():
            self.name = value
            self.save()