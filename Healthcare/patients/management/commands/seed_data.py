from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

from patients.models import Patient
from doctors.models import Doctor


PATIENT_SEED = [
    ("John Carter", 34, "Male", "Hypertension"),
    ("Ava Thompson", 28, "Female", "Asthma"),
    ("Liam Rodriguez", 45, "Male", "Diabetes"),
    ("Mia Patel", 31, "Female", "Thyroid"),
    ("Noah Kim", 52, "Male", "High cholesterol"),
    ("Sophia Nguyen", 26, "Female", "Anemia"),
    ("Ethan Brooks", 39, "Male", "Back pain"),
    ("Olivia Reed", 47, "Female", "Arthritis"),
    ("Mason Lee", 22, "Male", "Migraine"),
    ("Isabella Clark", 36, "Female", "Allergies"),
]

DOCTOR_SEED = [
    ("Dr. Priya Shah", "Cardiology", "priya.shah@example.com", "+1-555-555-1001"),
    ("Dr. Arjun Mehta", "Orthopedics", "arjun.mehta@example.com", "+1-555-555-1002"),
    ("Dr. Emily Stone", "Dermatology", "emily.stone@example.com", "+1-555-555-1003"),
    ("Dr. Samuel Wright", "Neurology", "samuel.wright@example.com", "+1-555-555-1004"),
    ("Dr. Chloe Martin", "Pediatrics", "chloe.martin@example.com", "+1-555-555-1005"),
    ("Dr. Daniel Park", "Psychiatry", "daniel.park@example.com", "+1-555-555-1006"),
    ("Dr. Grace Allen", "Endocrinology", "grace.allen@example.com", "+1-555-555-1007"),
    ("Dr. Henry Lopez", "Gastroenterology", "henry.lopez@example.com", "+1-555-555-1008"),
    ("Dr. Nora Adams", "ENT", "nora.adams@example.com", "+1-555-555-1009"),
    ("Dr. Victor Chen", "Oncology", "victor.chen@example.com", "+1-555-555-1010"),
]


class Command(BaseCommand):
    help = "Seed 10 doctors and 10 patients for quick testing."

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            type=str,
            default=None,
            help="Assign patients to this username/email. Defaults to first superuser or first user.",
        )
        parser.add_argument(
            "--count",
            type=int,
            default=10,
            help="Number of doctors/patients to create (max 10 with built-in seed data).",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        count = max(1, min(options["count"], 10))
        username = options["username"]

        user = None
        if username:
            user = User.objects.filter(username=username).first() or User.objects.filter(email=username).first()

        if not user:
            user = User.objects.filter(is_superuser=True).order_by("id").first()

        if not user:
            user = User.objects.order_by("id").first()

        if not user:
            user = User.objects.create_user(
                username="seed_user@example.com",
                email="seed_user@example.com",
                password="seedpassword123",
                first_name="Seed",
            )
            self.stdout.write(self.style.WARNING("Created default user: seed_user@example.com / seedpassword123"))

        created_doctors = 0
        for name, specialization, email, phone in DOCTOR_SEED[:count]:
            _, created = Doctor.objects.get_or_create(
                email=email,
                defaults={"name": name, "specialization": specialization, "phone": phone},
            )
            created_doctors += 1 if created else 0

        created_patients = 0
        for name, age, gender, history in PATIENT_SEED[:count]:
            _, created = Patient.objects.get_or_create(
                name=name,
                created_by=user,
                defaults={"age": age, "gender": gender, "medical_history": history},
            )
            created_patients += 1 if created else 0

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed complete. Doctors created: {created_doctors}, Patients created: {created_patients} (user: {user.username})"
            )
        )
