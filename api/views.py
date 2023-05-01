import json

from django.http.response import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from api.models import Company, Vacancy
from api.serializers import CompanySerializer, CompanyDetailSerializer,\
    CompanyListSerializer, VacancyListSerializer, \
    PostVacancySerializer, PostVacancyListSerializer,\
    PostVacancyDetailSerializer


class CompanyViewSet(viewsets.ModelViewSet):

    serializer_action_classes = {
        'list': CompanyListSerializer,
        'retrieve': CompanyDetailSerializer,
        'create': CompanySerializer,
        'update': CompanyDetailSerializer
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


# Vacancy function views
@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated, ))
def vacancies_view(request) -> Response:

    if request.method == 'GET':
        vacancies = Vacancy.objects.all()
        serializer = PostVacancyListSerializer(vacancies, many=True)
        return Response(serializer.data, status=200)

    if request.method == 'POST':
        data = json.loads(request.body)
        serializer = PostVacancyDetailSerializer(data=data)
        if serializer.is_valid():
            vacancy = Vacancy.objects.create(**serializer.data)
            vacancy_data = PostVacancyDetailSerializer(vacancy).data
            return Response(vacancy_data, status=201)
        return Response(serializer.errors, status=403)
    return Response({"error": "Not found"}, status=404)


@api_view(['PUT', 'DELETE', 'GET'])
@permission_classes((IsAuthenticated, ))
def vacancy_detail_view(request, pk) -> Response:

    if request.method == 'GET':
        try:
            vacancy = Vacancy.objects.get(pk=pk)
            serializer = PostVacancyDetailSerializer(vacancy)
            return Response(serializer.data, status=200)
        except Vacancy.DoesNotExist:
            return Response({'error': 'Vacancy did not found'}, status=404)

    if request.method == 'PUT':
        data = json.loads(request.body)
        serializer = PostVacancyDetailSerializer(data=data)
        if serializer.is_valid():
            Vacancy.objects.create(**serializer.data)
            return Response(serializer.data, status=204)
        return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        try:
            Vacancy.objects.get(pk=pk).delete()
            return Response({}, status=204)
        except Exception as err:
            pass

    return Response({'error': 'Unknown error'}, status=500)


def vacancy_top_ten(request) -> JsonResponse:
    if request.method == 'GET':
        vacancies_ordered = Vacancy.objects.order_by('-salary')[:10]
        data = [vacancy.to_json() for vacancy in vacancies_ordered]
        return JsonResponse({'result': data}, status=200)


class LoginUserView(TokenObtainPairView):
    permission_classes = [AllowAny]


class RegisterUserView(TokenObtainPairView):
    permission_classes = [AllowAny]
