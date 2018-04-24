from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.


# 
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, kepler_id, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not kepler_id:
            raise ValueError('The given kepler id must be set')
        user = self.model(kepler_id=kepler_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, kepler_id, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(kepler_id, password, **extra_fields)

    def create_superuser(self, kepler_id, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(kepler_id, password, **extra_fields)


class User(AbstractUser):
    username = None
    username_validator = UnicodeUsernameValidator()
    kepler_id = models.CharField(
        _('kepler id'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that kepler id already exists."),
        },
    )
    USERNAME_FIELD = 'kepler_id'
    objects = UserManager()
    REQUIRED_FIELDS = ['email']


class Skill(models.Model):
    """
     Kepler users skills
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, verbose_name="skill name",
                            help_text="name of skill you can offer")
    description = models.TextField(verbose_name="skill description",
                                   help_text="please describe the skill you mentioned above ", blank=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Kepler User skill"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.user.kepler_id

    class Meta:
        ordering = ["user"]
        verbose_name = "User profile"


