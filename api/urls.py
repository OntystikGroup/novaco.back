from django.urls import path
from rest_framework.routers import DefaultRouter
# from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_simplejwt.views import TokenObtainPairView
from api.views import CompanyViewSet, \
    vacancies_view, vacancy_detail_view, vacancy_top_ten, \
    LoginUserView, RegisterUserView, RefreshUserTokenView


company_router = DefaultRouter()
company_router.register(r'companies', CompanyViewSet, basename='company')

# vacancy_router = DefaultRouter()
# vacancy_router.register(r'vacancies', VacancyViewSet, basename='vacancy')

urlpatterns = company_router.urls
# urlpatterns += vacancy_router.urls

urlpatterns += [
    # path('companies/', CompanyViewSet.as_view({'get': 'list'})),
    # path('companies/<int:pk>', CompanyViewSet.as_view({'get': 'retrieve'})),
    # path('companies/<int:pk>/vacancies', company_vacancies),
    path('vacancies/', vacancies_view),
    path('vacancies/<int:pk>/', vacancy_detail_view),
    path('vacancies/top_ten/', vacancy_top_ten),
    path('login/', LoginUserView.as_view()),
    path('register/', RegisterUserView.as_view()),
    path('refresh/', RefreshUserTokenView.as_view()),
    # path('logout/', Log)
    # path('ss/', ObtainJSONWebToken.as_view())
]