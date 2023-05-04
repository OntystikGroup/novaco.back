import json

from django.http.response import JsonResponse
from django.db.models import Q
from django.db.models.functions import Lower
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from api.permissions import IsAuthenticatedStaffOrReadOnly
from api.models import Vacancy
from api.serializers import PostVacancyListSerializer, PostVacancyDetailSerializer


# Vacancy function views
@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticatedStaffOrReadOnly,))
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
@permission_classes((IsAuthenticatedStaffOrReadOnly,))
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


@api_view(["GET"])
@permission_classes([AllowAny])
def search_by_param(request) -> Response:
    query = request.query_params.get('query')
    if not query:
        return Response([], status=status.HTTP_200_OK)
    result = Vacancy.objects.annotate(
        lname=Lower('name'),
        lcompany_name=Lower('company__name')
    ).filter(Q(lname__contains=query) | Q(lcompany_name__contains=query))
    return Response(PostVacancyListSerializer(result, many=True).data, status=status.HTTP_200_OK)