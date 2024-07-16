from django.core.exceptions import ValidationError


def name_validator(value):
    for char in value:
        if not (char.isalpha() or char.isspace()):
            raise ValidationError('Name can only contain letters and spaces')
