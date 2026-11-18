
from django import forms

from .models import ExpenseGroup


class ExpenseGroupForm(forms.ModelForm):
    class Meta:
        model = ExpenseGroup
        fields = ["name", "description"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. College Friends",
                "maxlength": 100,
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "What is this group for?",
                "rows": 3,
            }),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if len(name) < 3:
            raise forms.ValidationError(
                "Group name must contain at least 3 characters."
            )

        return name


class AddGroupMemberForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter an existing Splitly username",
        })
    )

    def clean_username(self):
        username = self.cleaned_data["username"].strip()

        if not username:
            raise forms.ValidationError(
                "Please enter a username."
            )

        return username
