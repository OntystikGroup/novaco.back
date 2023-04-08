from django.shortcuts import render
from django.http import JsonResponse

from api.models import Company, Vacancy


# Create your views here.
def companies_list(request) -> JsonResponse:
    companies = Company.objects.all()
    data = [company.to_json() for company in companies]
    return JsonResponse(data={'result': data},status=200)


def company_detail(request, pk) -> JsonResponse:
    try:
        company = Company.objects.get(pk=pk)
        data = company.to_json(detailed=True)
        return JsonResponse({'result': data}, status=200)
    except Company.DoesNotExist:
        return JsonResponse({'error': 'Company did not found'}, status=404)
    return JsonResponse({'error': 'Unknown error'}, status=500)


def company_vacancies(request, pk) -> JsonResponse:
    try:
        company = Company.objects.get(pk=pk)
        vacancies = company.vacancies.all()
        data = [vacancy.to_json() for vacancy in vacancies]
        return JsonResponse({'result': data}, status=200)
    except Company.DoesNotExist:
        return JsonResponse({'error': 'Company did not found'}, status=404)
    return JsonResponse({'error': 'Unknown error'}, status=500)


def vacancy_list(request) -> JsonResponse:
    vacancies = Vacancy.objects.all()
    data = [vacancy.to_json() for vacancy in vacancies]
    return JsonResponse({'result': data}, status=200)


def vacancy_detail(request, pk) -> JsonResponse:
    try:
        vacancy = Vacancy.objects.get(pk=pk)
        data = vacancy.to_json(detailed=True)
        return JsonResponse({'result': data}, status=200)
    except Vacancy.DoesNotExist:
        return JsonResponse({'error': 'Vacancy did not found'}, status=404)
    return JsonResponse({'error': 'Unknown error'}, status=500)


def vacancy_top_ten(request) -> JsonResponse:
    vacancies_ordered = Vacancy.objects.order_by('-salary')[:10]
    data = [vacancy.to_json() for vacancy in vacancies_ordered]
    return JsonResponse({'result': data}, status=200)