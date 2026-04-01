from django import forms
from django.core.exceptions import ValidationError

from common.mixins import ReadOnlyFormFieldsMixin
from drivers.models import Driver
from teams.models import Team


class DriverFormBase(forms.ModelForm):
    class Meta:
        model = Driver
        exclude = ['total_points', 'podiums', 'wins', 'dnfs', 'wins', 'owner']

        widgets = {
            'nationality': forms.TextInput(attrs={'placeholder': 'Enter 2 letter ISO code'}),
            'image': forms.URLInput(attrs={'placeholder': 'Enter image URL'}),
            'rookie_status': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')])
        }

    def clean_team(self):
        team = self.cleaned_data.get("team")
        if not team:
            return team

        drivers = team.drivers.all()

        if self.instance.pk:
            drivers = drivers.exclude(pk=self.instance.pk)

        if drivers.count() >= 2:
            raise ValidationError("A team can have a maximum of 2 drivers!")

        return team

class DriverCreateForm(DriverFormBase):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['team'].queryset = Team.objects.filter(owner=user)

class DriverEditForm(DriverFormBase):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['team'].queryset = Team.objects.filter(owner=user)

class DriverDeleteForm(ReadOnlyFormFieldsMixin, DriverFormBase):
    pass
