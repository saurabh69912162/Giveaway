from django.db import models
import time
from datetime import timedelta,datetime
import uuid
from django.contrib.auth.models import User
from django.template.defaultfilters import truncatechars

class user_details(models.Model):
    username = models.CharField(max_length=150,blank=False)
    email = models.EmailField(max_length=255,unique=True,verbose_name='email address')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone  = models.IntegerField(blank=True)
    category = models.CharField(max_length=10, default='Creator')
    date_of_joining = models.DateTimeField(default=datetime.now, null=True)
    image = models.ImageField(upload_to='profile_images/',default='profile_images/default.png')

    def __str__(self):
        return self.username


class new_giveaway(models.Model):
    username = models.CharField(max_length=255)
    giveaway_id = models.UUIDField(unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=255,default="Closed")
    giveaway_title = models.CharField(max_length=150,blank=False)
    description = models.TextField(max_length=2250,blank=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    banner_image = models.ImageField(upload_to='banner/',default='banner/default.png')
    image1 = models.ImageField(upload_to='sideimages/',default='sideimages/default1.png',blank=True,)
    caption1 = models.CharField(max_length=20,blank=True)
    image2 = models.ImageField(upload_to='sideimages/',default='sideimages/default2.png',blank=True,)
    caption2 = models.CharField(max_length=20, blank=True)
    image3 = models.ImageField(upload_to='sideimages/',default='sideimages/default3.png',blank=True,)
    caption3 = models.CharField(max_length=20, blank=True)
    number_of_winners = models.IntegerField()

    def __str__(self):
        return self.giveaway_title

    @property
    def short_description(self):
        return truncatechars(self.description, 35)

    def save(self, *args, **kwargs):
        new_obj = giveaway_analytics()
        new_obj.giveaway_id = self.giveaway_id
        new_obj.giveaway_name = self.giveaway_title
        new_obj.save()

        obj = giveaway_rule()
        obj.giveaway_name = self.giveaway_title
        obj.username = user_details.objects.get(username=self.username)
        obj.giveaway_id = self.giveaway_id
        obj.sequence_number = -1
        obj.save()
        super(new_giveaway, self).save(*args, **kwargs)



# https://www.youtube.com/watch?v=8nBZjkZR9VU
# https://www.youtube.com/watch?v=xHApZe81oms
# https://www.youtube.com/watch?v=RSYHe-6oET8
# https://www.youtube.com/watch?v=91k6WR1SL3A
# https://www.youtube.com/watch?v=7AIOGsZeBvg
#

class winners(models.Model):
    giveaway_name = models.ForeignKey(new_giveaway, on_delete=models.CASCADE)
    giveaway_id = models.UUIDField(blank=False,default="c0b89d2e-cb31-47ec-b175-a0ee9e59d433")
    winner_name =  models.CharField(max_length=255)
    winner_email = models.CharField(max_length=255)
    winner_image = models.ImageField(upload_to='winners/', default='winners/default.png',blank=True)
    rank = models.IntegerField()


class giveaway_rule(models.Model):
    giveaway_name = models.CharField(max_length=255,blank=False)
    username = models.ForeignKey(user_details, on_delete=models.CASCADE,null=True)
    giveaway_id = models.UUIDField(blank=False,default="c0b89d2e-cb31-47ec-b175-a0ee9e59d433")
    sequence_number = models.IntegerField(blank=False)

    insta_profile_follow = models.CharField(max_length=1000,blank=True)
    insta_post = models.CharField(max_length=1000,blank=True)
    insta_comment = models.CharField(max_length=1000,blank=True)


    facebook_profile_like = models.CharField(max_length=1000,blank=True)
    facebook_post_like = models.CharField(max_length=1000,blank=True)
    facebook_post_comment = models.CharField(max_length=1000,blank=True)
    facebook_post_share = models.CharField(max_length=1000,blank=True)

    twitter_profile_follow = models.CharField(max_length=1000,blank=True)
    tweet_like = models.CharField(max_length=1000,blank=True)
    tweet_comment = models.CharField(max_length=1000,blank=True)
    retweet = models.CharField(max_length=1000,blank=True)

    youtube_subscibe = models.CharField(max_length=1000,blank=True)
    youtube_comment = models.CharField(max_length=1000,blank=True)
    youtube_like = models.CharField(max_length=1000,blank=True)
    youtube_share = models.CharField(max_length=1000,blank=True)

    go_to_this_link = models.CharField(max_length=1000,blank=True)
    completed = models.BooleanField(default=False)
    status = models.CharField(max_length=20,blank=True)


class entry(models.Model):
    user = models.CharField(max_length=255,blank=False)
    giveaway_title = models.CharField(max_length=150, blank=True)
    giveaway_id = models.UUIDField(blank=False,default="c0b89d2e-cb31-47ec-b175-a0ee9e59d433")
    start_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.giveaway_title = new_giveaway.objects.get(giveaway_id=self.giveaway_id)
        super(entry, self).save(*args, **kwargs)


class giveaway_analytics(models.Model):
    giveaway_id = models.UUIDField(blank=False, default="c0b89d2e-cb31-47ec-b175-a0ee9e59d433")
    giveaway_name = models.CharField(max_length=255)
    participants_count = models.IntegerField(default=0)
    completed = models.IntegerField(default=0)
    partial = models.IntegerField(default=0)

class comments(models.Model):
    name = models.CharField(max_length=255,blank=True)
    comment = models.TextField(max_length=5500, blank=True)
    url = models.CharField(max_length=500,blank=True)
    count = models.IntegerField(default=1)
    video_count = models.IntegerField(default=1)
    def __str__(self):
        return self.name