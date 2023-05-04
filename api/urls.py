from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView
from api.views import CompanyViewSet, \
    vacancies_view, vacancy_detail_view, vacancy_top_ten, \
    LoginUserView, RegisterUserView, VacancyRespondView, \
    search_by_param


company_router = DefaultRouter()
company_router.register(r'companies', CompanyViewSet, basename='company')

urlpatterns = company_router.urls

urlpatterns += [
    # path('companies/', CompanyViewSet.as_view({'get': 'list'})),
    # path('companies/<int:pk>', CompanyViewSet.as_view({'get': 'retrieve'})),
    # path('companies/<int:pk>/vacancies', company_vacancies),
    path('vacancies/', vacancies_view),
    path('vacancies/<int:pk>/', vacancy_detail_view),
    path('vacancies/top_ten/', vacancy_top_ten),
    path('search', search_by_param),
    path('auth/login/', LoginUserView.as_view()),
    path('auth/logout/', TokenBlacklistView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),
    path('auth/register/', RegisterUserView.as_view()),
    path('respond/', VacancyRespondView.as_view()),
]