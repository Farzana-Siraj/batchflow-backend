from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import APIException

from .models import Candidate


class ConflictException(APIException):
    status_code = 409
    default_detail = "Resource already exists."
    default_code = "conflict"


class CandidateCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Candidate
        fields = [
            "name",
            "email",
            "phone_number",
            "link",
            "dob",
        ]
        extra_kwargs = {
            "email": {"validators": []},
            "phone_number": {"validators": []},
        }

    def create(self, validated_data):
        try:
            return Candidate.objects.create(**validated_data)
        except IntegrityError:
            raise ConflictException(
                {"detail": "Candidate with this email or phone already exists."}
            )

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty.")
        return value
