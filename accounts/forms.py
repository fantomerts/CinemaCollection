from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        #user.email = self.cleaned_data["email"]
        user.email = get_email
        if commit:
            user.save()
        return user
    
    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data["email"]).exists():
            print(f'\n\n\n\n\n{self.cleaned_data["email"]}\n\n\n\n\n')
            raise forms.ValidationError("Email is not unique")
        else:
            global get_email
            get_email = self.cleaned_data["email"]