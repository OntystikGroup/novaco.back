from django.contrib import admin
from api.models import Vacancy, Company, User


# Register your models here.
admin.site.register(Vacancy)
admin.site.register(Company)
admin.site.register(User)