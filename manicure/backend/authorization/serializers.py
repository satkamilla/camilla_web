# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser as User, Master, Client

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_master', 'is_client')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    accountType = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'accountType', 'phone_number', 'city')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            city=validated_data['city']
        )
        user.set_password(validated_data['password'])
        
        if validated_data['accountType'] == 'master':
            user.is_master = True
            user.save()
            Master.objects.create(user=user)
        else:
            user.is_client = True
            user.save()
            Client.objects.create(user=user)
        
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")



class UserProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='get_full_name')
    picture = serializers.ImageField(source='profile_picture', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'picture', 'phone_number', 'is_master']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.is_master:
            master_profile = Master.objects.get(user=instance)
            representation['location'] = instance.city
            representation['bio'] = master_profile.description
        elif instance.is_client:
            client_profile = Client.objects.get(user=instance)
            representation['location'] = instance.city
            representation['bio'] = client_profile.description
        return representation
    
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(required=False)
    description = serializers.CharField(required=False)
    experience = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'city', 'profile_picture', 'age', 'description', 'experience']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.city = validated_data.get('city', instance.city)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()

        if instance.is_master:
            master_profile = Master.objects.get(user=instance)
            master_profile.age = validated_data.get('age', master_profile.age)
            master_profile.description = validated_data.get('description', master_profile.description)
            master_profile.experience = validated_data.get('experience', master_profile.experience)
            master_profile.save()
        elif instance.is_client:
            client_profile = Client.objects.get(user=instance)
            client_profile.age = validated_data.get('age', client_profile.age)
            client_profile.description = validated_data.get('description', client_profile.description)
            client_profile.save()
        
        return instance