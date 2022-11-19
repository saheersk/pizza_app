from .models import User
from rest_framework import serializers
from phonenumber_field.modelfields import PhoneNumberField


class UserCreationSerializer(serializers.ModelSerializer):
    username=serializers.CharField(max_length=25)
    email=serializers.EmailField(max_length=80)
    phone_number=PhoneNumberField(null=False, blank=False)
    password=serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model=User
        fields=['username', 'email', 'phone_number', 'password']

    def validate(self, attrs):
        username_exists=User.objects.filter(username=attrs['username']).exists()

        if username_exists:
            raise serializers.ValidationError(detail="User with username already exists")

        email_exists=User.objects.filter(username=attrs['email']).exists()

        if email_exists:
            raise serializers.ValidationError(detail="User with email already exists")

        phone_number_exists=User.objects.filter(username=attrs['phone_number']).exists()

        if phone_number_exists:
            raise serializers.ValidationError(detail="User with phone_number already exists")

        return super().validate(attrs)