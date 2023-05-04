from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView
from customAuth.views import LoginUserView, RegisterUserView

urlpatterns = [
    path('login/', LoginUserView.as_view()),
    path('logout/', TokenBlacklistView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('register/', RegisterUserView.as_view()),
]