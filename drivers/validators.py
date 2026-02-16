from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from teams.models import Team


@deconstructible
class AvailableSlotValidator:
    def __init__(self, max_value: int, message: str) -> None:
        self.max_value = max_value
        self.message = message

    @property
    def max_value(self):
        return self._max_value

    @max_value.setter
    def max_value(self, value):
        if value < 1:
            raise ValueError(f"Maximum value must be greater than 0")

        self._max_value = value

    def __call__(self, value: Team):
        if value.drivers.count() >= self.max_value:
            raise ValidationError(self.message)
