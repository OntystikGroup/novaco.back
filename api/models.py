from django.db import models
from django.contrib.auth.models import\
    AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.conf import settings


# Create your models here.
class Company(models.Model):

    name = models.CharField(max_length=100)
    logo_url = models.TextField(null=True)
    description = models.TextField()
    city = models.CharField(max_length=50)
    address = models.TextField()

    def __str__(self):
        return self.name

    def to_json(self, detailed=False) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'address': self.address,
        } if detailed else {
            'id': self.id,
            'name': self.name
        }


class Vacancy(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()
    salary = models.FloatField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')

    def __str__(self):
        return self.name

    def to_json(self, detailed=False) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'company': self.company.name,
            'description': self.description,
            'salary': self.salary
        } if detailed else {
            'id': self.id,
            'name': self.name,
            'salary': self.salary
        }


class UserManager(BaseUserManager):
    def create_user(self, username: str, password: str) -> 'User':
        if username is None:
            raise TypeError('Users must have a username.')

        if password is None:
            raise TypeError('Users must have a password.')

        user = self.model(username=username)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username: str, password: str) -> 'User':
        user = self.create_user(username=username, password=password)
        user.is_superuser = True
        user.is_active = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False, null=False)

    USERNAME_FIELD = 'username'
    objects = UserManager()


    def __str__(self):
        return f'{self.username}'

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}
