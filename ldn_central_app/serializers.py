from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Gym


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance


class GymSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    gym_details = serializers.CharField(required=True)
    gym_link = serializers.URLField(required=True)
    description = serializers.CharField(required=True)
    quality = serializers.CharField(required=True)
    access = serializers.CharField(required=True)
    network = serializers.CharField(required=True)
    contract = serializers.CharField(required=True)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)

    class Meta:
        model = Gym
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
