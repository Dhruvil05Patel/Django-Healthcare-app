from rest_framework import serializers
from .models import PatientDoctorMapping

class MappingSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.name", read_only=True)
    doctor_name = serializers.CharField(source="doctor.name", read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = ("id", "patient", "doctor", "patient_name", "doctor_name", "assigned_at")
        read_only_fields = ("assigned_at",)

    def validate(self, attrs):
        request = self.context.get("request")
        patient = attrs.get("patient")
        doctor = attrs.get("doctor")

        if request and patient and patient.created_by_id != request.user.id:
            raise serializers.ValidationError({"patient": "You do not own this patient."})

        if patient and doctor:
            if PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists():
                raise serializers.ValidationError("This doctor is already assigned to this patient.")

        return attrs
