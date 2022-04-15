from django.contrib.auth import models as auth_models, get_user_model
from django.core.validators import MinLengthValidator
from django.db import models
from softuni_web_project.accounts.managers import CustomUserManager
from softuni_web_project.tools.validators import validate_only_letters, \
    validate_only_letters_digits_underscores_and_dots, \
    validate_only_lowercase


class CustomUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    USERNAME_MAX_LENGTH = 30
    USERNAME_MIN_LENGTH = 3

    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        validators=(
            MinLengthValidator(3),
            validate_only_letters_digits_underscores_and_dots,
            validate_only_lowercase,
        )
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'username'

    objects = CustomUserManager()


UserModel = get_user_model()


class Country(models.Model):
    COUNTRY_NAME_MAX_LENGTH = 50
    name = models.CharField(
        max_length=COUNTRY_NAME_MAX_LENGTH,
        unique=True,
    )

    def __str__(self):
        return self.name


class Profile(models.Model):
    FIRST_NAME_MAX_LENGTH = 30
    FIRST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAX_LENGTH = 30
    LAST_NAME_MIN_LENGTH = 2

    MALE = 'Male'

    FEMALE = 'Female'

    DO_NOT_SHOW = 'Do not show'

    GENDERS = [(x, x) for x in (MALE, FEMALE, DO_NOT_SHOW)]

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            validate_only_letters,
        ),
        null=True,
        blank=True,
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LENGTH),
            validate_only_letters,
        ),
        null=True,
        blank=True,
    )

    picture = models.ImageField(
        null=True,
        blank=True,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    bio = models.TextField(
        null=True,
        blank=True
    )

    email = models.EmailField(
        null=True,
        blank=True
    )

    gender = models.CharField(
        max_length=max([len(x[0]) for x in GENDERS]),
        choices=GENDERS,
        null=True,
        blank=True,
        default=DO_NOT_SHOW,
    )

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    following = models.ManyToManyField(
        'self',
        related_name='following_profiles',
        symmetrical=False,
        null=True,
        blank=True,
    )

    followers = models.ManyToManyField(
        'self',
        related_name='followers_profiles',
        symmetrical=False,
        null=True,
        blank=True,
    )

    def __str__(self):
        username = UserModel.objects.get(id=self.user_id).username
        return username

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
