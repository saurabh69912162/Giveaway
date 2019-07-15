from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import *
from django import forms
from datetime import datetime
from django.apps import apps




class data_form(forms.ModelForm):
    class Meta:
        model = apps.get_model('details', 'entry')
        fields = "__all__"


class rules_form(forms.ModelForm):
    class Meta:
        model = apps.get_model('details', 'giveaway_rule')
        fields = ('sequence_number','insta_profile_follow','insta_post','insta_comment','facebook_profile_like',
                  'facebook_post_like','facebook_post_comment','facebook_post_share','twitter_profile_follow',
                  'tweet_like','tweet_comment','retweet','youtube_subscibe','youtube_comment',
                  'youtube_like','youtube_share','go_to_this_link')

