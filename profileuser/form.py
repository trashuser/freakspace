from django.forms import ModelForm
from blog.models import UserProfile

class EditUserProfile(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']