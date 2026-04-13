from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ("id", "name", "age", "gender", "medical_history", "created_at")
        read_only_fields = ("created_at",)