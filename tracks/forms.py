from django import forms

from common.mixins import ReadOnlyFormFieldsMixin
from tracks.models import Track


class TrackBaseForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = '__all__'

class TrackCreateForm(TrackBaseForm):
    pass

class TrackUpdateForm(TrackBaseForm):
    pass

class TrackDeleteForm(ReadOnlyFormFieldsMixin, TrackBaseForm):
    pass
