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
