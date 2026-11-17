import re

from django import forms

from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Enquiry
        fields = ["name", "phone", "email", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name", "maxlength": "120"}),
            "phone": forms.TextInput(
                attrs={"autocomplete": "tel", "inputmode": "tel", "maxlength": "20"}
            ),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "message": forms.Textarea(attrs={"rows": 4, "maxlength": "2000"}),
        }

    def clean_phone(self):
        phone = re.sub(r"[\s().+-]", "", self.cleaned_data["phone"])
        if not phone.isdigit() or not 7 <= len(phone) <= 15:
            raise forms.ValidationError("Enter a valid phone number, including country code if needed.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("website"):
            raise forms.ValidationError("We could not submit this enquiry. Please try again.")
        return cleaned_data
