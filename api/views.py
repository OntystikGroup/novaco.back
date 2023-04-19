import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
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
@csrf_exempt
def vacancies_view(request) -> JsonResponse:

    if request.method == 'GET':
        vacancies = Vacancy.objects.all()
        serializer = PostVacancyListSerializer(vacancies, many=True)
        return JsonResponse({'result': serializer.data}, status=200)

    if request.method == 'POST':
        data = json.loads(request.body)
        serializer = PostVacancyDetailSerializer(data=data)
        if serializer.is_valid():
            vacancy = Vacancy.objects.create(**serializer.data)
            vacancy_data = PostVacancyDetailSerializer(vacancy).data
            return JsonResponse({"result": vacancy_data}, status=201)
        return JsonResponse(serializer.errors, status=403)
    return JsonResponse({"error": "Not found"}, status=404)


@csrf_exempt
def vacancy_detail_view(request, pk) -> JsonResponse:

    if request.method == 'GET':
        try:
            vacancy = Vacancy.objects.get(pk=pk)
            serializer = PostVacancyDetailSerializer(vacancy)
            return JsonResponse({'result': serializer.data}, status=200)
        except Vacancy.DoesNotExist:
            return JsonResponse({'error': 'Vacancy did not found'}, status=404)

    if request.method == 'PUT':
        data = json.loads(request.body)
        serializer = PostVacancyDetailSerializer(data=data)
        if serializer.is_valid():
            Vacancy.objects.create(**serializer.data)
            return JsonResponse({'result': serializer.data}, status=204)
        return JsonResponse(serializer.errors, status=400)

    if request.method == 'DELETE':
        try:
            Vacancy.objects.get(pk=pk).delete()
            return JsonResponse({}, status=204)
        except Exception as err:
            pass

    return JsonResponse({'error': 'Unknown error'}, status=500)


def vacancy_top_ten(request) -> JsonResponse:
    vacancies_ordered = Vacancy.objects.order_by('-salary')[:10]
    data = [vacancy.to_json() for vacancy in vacancies_ordered]
    return JsonResponse({'result': data}, status=200)


# class VacancyViewSet(viewsets.ModelViewSet):
#
#     serializer_action_classes = {
#         'list': VacancyListSerializer,
#         'retrieve': VacancyDetailSerializer,
#         'create': VacancySerializer,
#         'update': VacancyDetailSerializer,
#     }
#
#     def get_serializer_class(self):
#         return self.serializer_action_classes[self.action]
#
#     @action(detail=False, methods=['GET'])
#     def top_ten(self, request):
#         vacancies = Vacancy.objects.all().order_by('-salary')[:10]
#         serializer = VacancyListSerializer(vacancies, many=True)
#         return Response(serializer.data)
#
#     def get_queryset(self):
#         return Vacancy.objects.all()


# def company_detail(request, pk) -> JsonResponse:
#     try:
#         company = Company.objects.get(pk=pk)
#         data = company.to_json(detailed=True)
#         return JsonResponse({'result': data}, status=200)
#     except Company.DoesNotExist:
#         return JsonResponse({'error': 'Company did not found'}, status=404)
#     return JsonResponse({'error': 'Unknown error'}, status=500)
#
#
# def company_vacancies(request, pk) -> JsonResponse:
#     try:
#         company = Company.objects.get(pk=pk)
#         vacancies = company.vacancies.all()
#         data = [vacancy.to_json() for vacancy in vacancies]
#         return JsonResponse({'result': data}, status=200)
#     except Company.DoesNotExist:
#         return JsonResponse({'error': 'Company did not found'}, status=404)
#     return JsonResponse({'error': 'Unknown error'}, status=500)


