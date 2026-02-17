from django import forms
from common.mixins import ReadOnlyFormFieldsMixin
from drivers.models import Driver


class DriverFormBase(forms.ModelForm):
    class Meta:
        model = Driver
        exclude = ['total_points', 'podiums', 'wins', 'dnfs', 'wins']

class DriverCreateForm(DriverFormBase):
    pass

class DriverEditForm(DriverFormBase):
    pass

class DriverDeleteForm(ReadOnlyFormFieldsMixin, DriverFormBase):
    pass
