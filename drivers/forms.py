from django import forms
from common.mixins import ReadOnlyFormFieldsMixin
from drivers.models import Driver


class DriverFormBase(forms.ModelForm):
    class Meta:
        model = Driver
        exclude = ['total_points', 'podiums', 'wins', 'dnfs', 'wins']

        widgets = {
            'nationality': forms.TextInput(attrs={'placeholder': 'Enter 2 letter ISO code'}),
            'image': forms.URLInput(attrs={'placeholder': 'Enter image URL'}),
            'rookie_status': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')])
        }

class DriverCreateForm(DriverFormBase):
    pass

class DriverEditForm(DriverFormBase):
    pass

class DriverDeleteForm(ReadOnlyFormFieldsMixin, DriverFormBase):
    pass
