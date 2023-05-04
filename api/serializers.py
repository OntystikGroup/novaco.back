from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer
from rest_framework_simplejwt.tokens import AccessToken
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


class LoginUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'password' ,'tokens', 'is_staff']

    def get_tokens(self, obj):
        user = User.objects.get(username=obj.username)
        return user.tokens

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if password is None:
            raise serializers.ValidationError("Password is required")

        if username is None:
            raise serializers.ValidationError("Username is required")

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError('A user with this username and password was not found.')

        if not user.is_active:
            raise serializers.ValidationError('This user is not currently activated.')

        return user


class RegisterUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],
                                        password=validated_data['password'])
        return user

    def validate(self, attrs):
        is_user_exists = User.objects.filter(username=attrs['username']).exists()
        if is_user_exists:
            raise serializers.ValidationError("User exists")
        return attrs


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=255)


class LoggedUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=255)
    tokens = serializers.SerializerMethodField()
    is_staff = serializers.BooleanField()

    class Meta:
        model = User

    def get_tokens(self, obj):
        return obj.get('tokens')


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
