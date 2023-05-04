from django.db import models
from django.contrib.auth.models import\
    AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager
from customAuth.models import User


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


class RespondManager(models.Manager):
    def create_respond(self, user_id, vacancy_id):
        user = User.objects.get(pk=user_id)
        vacancy = Vacancy.objects.get(pk=vacancy_id)

        respond = Respond(user=user, vacancy=vacancy)
        respond.save()

        return respond


class Respond(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responds')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='vacancy')
    respond_at = models.DateTimeField(auto_now_add=True)

    objects = RespondManager()

    class Meta:
        unique_together = (('user', 'vacancy'),)

    @property
    def vacancy_name(self):
        return self.vacancy.name

    @property
    def expecting_salary(self):
        return self.vacancy.salary

    @property
    def company(self):
        return self.vacancy.company.name
