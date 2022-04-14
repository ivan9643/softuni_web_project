from django.core.exceptions import ValidationError


def validate_only_letters(value):
    for ch in value:
        if not ch.isalpha():
            raise ValidationError('Value must contain only letters')


def validate_only_lowercase(value):
    if value.lower() != value:
        raise ValidationError('Value must contain only lowercase letters')


def validate_only_letters_digits_underscores_and_dots(value):
    for ch in value:
        if not ch.isalpha() and not ch.isdigit() and not ch == '_' and not ch == '.':
            raise ValidationError('Value must contain only letters, digits, underscores and dots')

