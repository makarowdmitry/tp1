from django import forms
from models import *
from django.contrib.auth import get_user_model
from tp.widgets import *


class AddPhoto(forms.ModelForm):
    class Meta:
        model = Photo
        widgets = {'image':MultiFileInput}

class ChangePhoto(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']


class SignupForm(forms.Form):

    sex = forms.CharField(widget=forms.HiddenInput, initial='men')

    class Meta:
        model = get_user_model()

    def save(self, user):
        user.save()
        profile = UserProfile(
            user=user,
            sex=1 if self.cleaned_data['sex'] == 'men' else 0,
            phone=' '
        )
        profile.save()


class ProfileImageForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['image']


class ItemPhoto(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']
