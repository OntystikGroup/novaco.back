from django.contrib import admin
from api.models import Vacancy, Company, Resume


# Register your models here.
admin.site.register(Vacancy)
admin.site.register(Company)
admin.site.register(Resume)