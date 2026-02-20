from django import forms
from django.core.exceptions import ValidationError

from common.mixins import ReadOnlyFormFieldsMixin
from races.models import Race, Result


# Base forms
class RaceFormBase(forms.ModelForm):
    class Meta:
        model = Race
        exclude = ['created_at', 'updated_at', 'drivers']
        widgets = {
            "date": forms.DateTimeInput(attrs={
                "type": "datetime-local",
                "class": "form-control datetime-input",
            })
        }

class ResultFormBase(forms.ModelForm):
    class Meta:
        model = Result
        fields = '__all__'
        widgets = {
            'fastest_lap': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
        }

    def clean(self) -> None:
        cleaned = super().clean()

        finishing_position = cleaned.get('finishing_position')
        status = cleaned.get('status')

        if finishing_position is not None and status != 'Finished':
            raise ValidationError(f'If status is not "Finished", finishing position must be null ')
        if finishing_position is None and status == 'Finished':
            raise ValidationError(f'If status is "Finished", finishing position cannot be null ')

# Race forms

class RaceCreateForm(RaceFormBase):
    pass

class RaceEditForm(RaceFormBase):
    pass

class RaceDeleteForm(ReadOnlyFormFieldsMixin, RaceFormBase):
    pass

# Result forms

class ResultCreateForm(ResultFormBase):
    pass

class ResultEditForm(ResultFormBase):
    pass

class ResultDeleteForm(ReadOnlyFormFieldsMixin, ResultFormBase):
    pass
