from django import forms


class ContactForm(forms.Form):
    fullname = forms.CharField(
        label="Name",
        widget=forms.TextInput
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput
    )
    content = forms.CharField(
        label="Content",
        widget=forms.Textarea(
            attrs={
                "rows": "4",
            }
        )
    )
