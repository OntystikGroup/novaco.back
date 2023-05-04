from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from api.models import Company
from api.serializers import (CompanySerializer, CompanyDetailSerializer,
                             CompanyListSerializer, VacancyListSerializer,
                             LoginUserSerializer, RegisterUserSerializer,
                             UserSerializer, LoggedUserSerializer,
                             VacancyRespondSerializer, RespondListSerializer)
from api.permissions import IsAuthenticatedStaffOrReadOnly


class CompanyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedStaffOrReadOnly]
    serializer_action_classes = {
        'list': CompanyListSerializer,
        'retrieve': CompanyDetailSerializer,
        'create': CompanySerializer,
        'partial_update': CompanyDetailSerializer
    }

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]

    @action(detail=True, methods=['GET'])
    def vacancies(self, request, pk=None):
        company = self.get_object()
        vacancies = company.vacancies.all()
        serializer = VacancyListSerializer(vacancies, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return Company.objects.all()


class LoginUserView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        user = request.data
        serializer = self.serializer_class(data=user)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(LoggedUserSerializer(serializer.data).data, status=status.HTTP_200_OK)


class RegisterUserView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            user = serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(UserSerializer(serializer.data).data, status=status.HTTP_200_OK)


class VacancyRespondView(APIView):

    def post(self, request):
        data = request.data
        data['user_id'] = request.user.id
        serializer = VacancyRespondSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        user = request.user
        responds = user.responds.all()
        serializer = RespondListSerializer(responds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

