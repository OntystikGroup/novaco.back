from rest_framework import serializers
from api.models import Company, Vacancy


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'description', 'city', 'address']


class CompanyDetailSerializer(CompanySerializer):
    class Meta(CompanySerializer.Meta):
        fields = '__all__'


class CompanyListSerializer(CompanySerializer):
    class Meta(CompanySerializer.Meta):
        fields = ['id', 'name']


class PostVacancySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(min_length=1)
    salary = serializers.FloatField()
    company = serializers.IntegerField()


class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__'


class VacancyListSerializer(VacancySerializer):
    class Meta(VacancySerializer.Meta):
        fields = ['id', 'name', 'salary']


class VacancyDetailSerializer(VacancySerializer):
    class Meta(VacancySerializer.Meta):
        model = Vacancy
        fields = '__all__'