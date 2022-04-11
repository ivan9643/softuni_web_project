from django.core.exceptions import ValidationError


def validate_only_letters(value):
    for ch in value:
        if not ch.isalpha():
            raise ValidationError('Value must contain only letters')


# def validate_file_max_size(max_size):
#     def validate(value):
#         filesize = value.file.size
#         megabyte_limit = max_size
#         if filesize > megabyte_limit * 1024 * 1024:
#             raise ValidationError('Max file size is %sMB' % str(megabyte_limit))
#
#     return validate

