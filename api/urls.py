from django.urls import path
from api.views import (companies_list, company_detail,
                       company_vacancies, vacancy_list,
                       vacancy_detail, vacancy_top_ten)

urlpatterns = [
    path('companies/', companies_list),
    path('companies/<int:pk>', company_detail),
    path('companies/<int:pk>/vacancies', company_vacancies),
    path('vacancies/', vacancy_list),
    path('vacancies/<int:pk>', vacancy_detail),
    path('vacancies/top_ten/', vacancy_top_ten),
]