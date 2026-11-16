
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import User


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        required=True
    )
    last_name = forms.CharField(
        max_length=150,
        required=True
    )
    email = forms.EmailField(
        required=True
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'contact_number',
            'password1',
            'password2',
        ]

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError(
                "This email address is already registered."
            )

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = 'member'
        user.is_staff = False
        user.is_superuser = False

        if commit:
            user.save()

        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'contact_number',
        ]

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        if User.objects.filter(
            email__iexact=email
        ).exclude(
            pk=self.instance.pk
        ).exists():
            raise ValidationError(
                "This email address is already in use."
            )

        return email
