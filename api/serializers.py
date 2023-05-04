from rest_framework import serializers
from api.models import Company, Vacancy, User, Respond


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'description', 'city', 'address', 'logo_url']


class CompanyDetailSerializer(CompanySerializer):
    class Meta(CompanySerializer.Meta):
        fields = '__all__'


class CompanyListSerializer(CompanySerializer):
    class Meta(CompanySerializer.Meta):
        fields = ['id', 'name']


class PostVacancySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(min_length=1)
    salary = serializers.FloatField()
    company = serializers.SerializerMethodField()

    def get_company(self, obj):
        return obj.company.name


class PostVacancyListSerializer(PostVacancySerializer):
    description = None
    company_id = None


class PostVacancyDetailSerializer(PostVacancySerializer):
    pass


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


class VacancyRespondSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    vacancy_id = serializers.IntegerField()

    def validate(self, attrs):
        user_id = attrs['user_id']
        vacancy_id = attrs['vacancy_id']

        try:
            User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this id does not exists")
        try:
            Vacancy.objects.get(id=vacancy_id)
        except Vacancy.DoesNotExist:
            raise serializers.ValidationError("Vacancy with this id does not exists")

        if Respond.objects.filter(user_id=user_id, vacancy_id=vacancy_id).exists():
            raise serializers.ValidationError("Respond exists")
        return attrs

    def create(self, validated_data):
        respond = Respond.objects.create_respond(**validated_data)
        return respond


class RespondListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respond
        fields = [
            'vacancy_name', 'expecting_salary',
            'company', 'respond_at']
