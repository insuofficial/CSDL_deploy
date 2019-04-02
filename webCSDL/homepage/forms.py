from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'last_name', 'first_name')

class ProfileForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class Projectform(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('__all__')


class Journalform(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ('__all__')

class Conferenceform(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ('__all__')

class Patentform(forms.ModelForm):
    class Meta:
        model = Patent
        fields = ('__all__')


class Noticeform(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Notice
        fields = ('title', 'content', ) # "__all__"

class Seminarform(forms.ModelForm):
    class Meta:
        model = Seminar
        fields = ('__all__')

class Albumform(forms.ModelForm):
    class Meta:
        image = forms.ImageField()
        model = Album
        fields = ('__all__')


'''
class PostAdmin(admin.ModelAdmin):
    form = Postform

admin.site.register(Post, PostAdmin)
'''