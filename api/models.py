from django.db import models
from django.contrib.auth.models import AbstractUser, User

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


class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='resume')
    experience_year = models.IntegerField(null=True)
    skills = models.CharField(max_length=255, null=True)
    preferred_salary = models.FloatField(null=True)
