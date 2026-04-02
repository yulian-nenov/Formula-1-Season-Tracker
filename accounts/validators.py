import math

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class MaxSizeValidator:
    def __init__(self, max_size):
        self.max_size = max_size

    @property
    def max_size(self):
        return self._max_size

    @max_size.setter
    def max_size(self, value):
        if value <= 0:
            raise ValueError('Max size must be greater than 0')

        self._max_size = value

    def __call__(self, value):
        size_mb = math.ceil(value.size / (1024 * 1024))
        if size_mb > self.max_size:
            raise ValidationError(f'Maximum file size is {self.max_size} MB!')