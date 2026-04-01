from django.contrib.auth.mixins import UserPassesTestMixin


class ReadOnlyFormFieldsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].disabled = True

class OwnerOnlyMixin(UserPassesTestMixin):
    owner_field = "owner"

    def test_func(self):
        obj = self.get_object()
        owner = getattr(obj, self.owner_field)
        return self.request.user.is_superuser or owner == self.request.user
