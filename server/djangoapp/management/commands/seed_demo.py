from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from djangoapp.models import CarMake, CarModel


DEMO_CARS = {
    "Toyota": ["Camry", "RAV4"],
    "Honda": ["Accord", "CR-V"],
    "Ford": ["Mustang", "Explorer"],
    "Tesla": ["Model 3", "Model Y"],
}


class Command(BaseCommand):
    help = "Create deterministic demo users, car makes, and car models."

    def handle(self, *args, **options):
        root, _ = User.objects.get_or_create(
            username="root",
            defaults={
                "email": "root@bestcars.example",
                "first_name": "Root",
                "last_name": "Administrator",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        root.is_staff = True
        root.is_superuser = True
        root.set_password("RootPass123!")
        root.save()

        for make_name, model_names in DEMO_CARS.items():
            make, _ = CarMake.objects.get_or_create(
                name=make_name,
                defaults={"description": f"Popular {make_name} vehicles."},
            )
            for index, model_name in enumerate(model_names):
                CarModel.objects.get_or_create(
                    car_make=make,
                    name=model_name,
                    defaults={
                        "dealer_id": index + 1,
                        "type": CarModel.SUV if index else CarModel.SEDAN,
                        "year": 2026,
                    },
                )

        self.stdout.write(self.style.SUCCESS("Demo data is ready."))
