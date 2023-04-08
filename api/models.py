from django.db import models


# Create your models here.
class Company(models.Model):

    name = models.CharField(max_length=100)
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


