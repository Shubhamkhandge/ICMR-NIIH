from django import forms
from captcha.fields import CaptchaField, CaptchaTextInput

from django.contrib.auth.models import User

    
class UserForm(forms.ModelForm):
    class Meta:
    	model = User
    	fields = ['username', 'password']
     
     
     
class CaptchaForm(forms.Form):

    captcha = CaptchaField()
    widget = CaptchaTextInput(attrs={
        "class":"from-control",
        'style': 'margin:10px',
        'max-width': '100px',
        'margin-top': '8px'
    })
    

captcha_form = CaptchaForm()