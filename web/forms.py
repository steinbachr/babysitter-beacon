from django import forms
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth import authenticate
from web.models import *
import pdb


class LoginForm(forms.Form):
    email = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.target = kwargs.pop('target')  # should be either a Parent or Sitter class reference
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned = super(LoginForm, self).clean()
        email, password = cleaned.get('email'), cleaned.get('password')

        try:
            user = self.target.objects.get(email__iexact=email)
            user = authenticate(cls=self.target, email=email, password=password)
            if user is None:
                raise forms.ValidationError("Incorrect password given")
        except ObjectDoesNotExist:
            raise forms.ValidationError("Incorrect email/password given")

        return cleaned


class SignupForm(forms.ModelForm):
    def clean(self):
        cleaned = super(SignupForm, self).clean()
        cleaned_email = cleaned.get('email')

        if self._meta.model.objects.filter(email=cleaned_email).exists():
            raise forms.ValidationError("You've already signed up. Please Log in")

        return cleaned


class ParentSignupForm(SignupForm):
    class Meta:
        model = Parent
        fields = ['email', 'password', 'first_name', 'last_name', 'phone_number']
        widgets = {
            'password': forms.PasswordInput
        }


class SitterSignupForm(SignupForm):
    class Meta:
        model = Sitter
        fields = ['email', 'password', 'first_name', 'last_name', 'phone_number', 'age']
        widgets = {
            'password': forms.PasswordInput
        }


class PaymentForm(forms.Form):
    stripe_token = forms.CharField(required=True, widget=forms.HiddenInput)
    card_number = forms.CharField(required=False)
    cvc = forms.CharField(required=False)
    expiration_month = forms.CharField(required=False)
    expiration_year = forms.CharField(required=False)


#####-----< Parent Forms >-----#####


class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        exclude = ['image']
        widgets = {
            'parent': forms.HiddenInput
        }


class BeaconForm(forms.ModelForm):
    class Meta:
        model = Beacon
        exclude = ['created_time']
        widgets = {
            'created_by': forms.HiddenInput
        }


class ParentProfileForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['address', 'city', 'state', 'postal_code']