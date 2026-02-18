from django import forms

from common.mixins import ReadOnlyFormFieldsMixin
from races.models import Race


# Base forms
class RaceFormBase(forms.ModelForm):
    class Meta:
        model = Race
        exclude = ['created_at', 'updated_at', 'drivers']
        widgets = {
            "date": forms.DateTimeInput(attrs={
                "type": "datetime-local",
                "class": "form-control datetime-input"
            })
        }

class RaceCreateForm(RaceFormBase):
    pass

class RaceEditForm(RaceFormBase):
    pass

class RaceDeleteForm(ReadOnlyFormFieldsMixin, RaceFormBase):
    pass
