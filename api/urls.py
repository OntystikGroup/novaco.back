from django.urls import path
from rest_framework.routers import DefaultRouter
from api.views import CompanyViewSet, \
    vacancies_view, vacancy_detail_view, vacancy_top_ten, \
    VacancyRespondView, search_by_param


company_router = DefaultRouter()
company_router.register(r'companies', CompanyViewSet, basename='company')

urlpatterns = company_router.urls

urlpatterns += [
    path('vacancies/', vacancies_view),
    path('vacancies/<int:pk>/', vacancy_detail_view),
    path('vacancies/top_ten/', vacancy_top_ten),
    path('search', search_by_param),
    path('respond/', VacancyRespondView.as_view()),
]