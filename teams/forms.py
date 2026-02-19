from django import forms
from common.mixins import ReadOnlyFormFieldsMixin
from teams.models import Team, CarModel


class TeamFormBase(forms.ModelForm):
    class Meta:
        model = Team
        exclude = ['created_at', 'updated_at']

class CarFormBase(forms.ModelForm):
    class Meta:
        model = CarModel
        exclude = ["team", 'id']
        widgets = {
            'in_use': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')])
        }

class TeamCreateForm(TeamFormBase):
    pass

class CarCreateForm(CarFormBase):
    pass

class TeamEditForm(TeamFormBase):
    pass

class CarEditForm(CarFormBase):
    pass

class TeamDeleteForm(ReadOnlyFormFieldsMixin, TeamFormBase):
    pass

class CarDeleteForm(ReadOnlyFormFieldsMixin, CarFormBase):
    pass

