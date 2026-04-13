from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import PatientDoctorMapping
from .serializers import MappingSerializer

class MappingViewSet(viewsets.ModelViewSet):
    queryset = PatientDoctorMapping.objects.select_related("patient", "doctor").all()
    serializer_class = MappingSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "delete"]  # No PUT/PATCH on mappings

    def get_queryset(self):
        return self.queryset.filter(patient__created_by=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        patient_id = kwargs.get("pk")
        mappings = self.get_queryset().filter(patient_id=patient_id)
        serializer = self.get_serializer(mappings, many=True)
        return Response(serializer.data)
