import json

from django.contrib.auth.models import User
from django.test import TestCase

from .management.commands.seed_demo import DEMO_CARS
from .models import CarMake, CarModel


class DealershipApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="capstone",
            password="CapstonePass123!",
            first_name="Capstone",
            last_name="Student",
            email="capstone@example.com",
        )
        make = CarMake.objects.create(name="Toyota", description="Reliable cars")
        CarModel.objects.create(car_make=make, name="Camry", year=2026)

    def test_login_and_logout(self):
        response = self.client.post(
            "/djangoapp/login",
            data=json.dumps({"userName": "capstone", "password": "CapstonePass123!"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "Authenticated")
        self.assertEqual(response.json()["firstName"], "Capstone")

        response = self.client.get("/djangoapp/logout")
        self.assertEqual(response.json()["status"], "Logged out")

    def test_registration(self):
        response = self.client.post(
            "/djangoapp/register",
            data=json.dumps({
                "userName": "newuser",
                "firstName": "New",
                "lastName": "User",
                "email": "new@example.com",
                "password": "NewUserPass123!",
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "Authenticated")

    def test_dealer_endpoints(self):
        all_dealers = self.client.get("/djangoapp/get_dealers").json()
        self.assertEqual(all_dealers["status"], 200)
        self.assertGreater(len(all_dealers["dealers"]), 20)

        kansas = self.client.get("/djangoapp/get_dealers/Kansas").json()
        self.assertTrue(kansas["dealers"])
        self.assertTrue(all(item["state"] == "Kansas" for item in kansas["dealers"]))

        dealer_id = kansas["dealers"][0]["id"]
        details = self.client.get(f"/djangoapp/dealer/{dealer_id}").json()
        self.assertEqual(details["dealer"][0]["id"], dealer_id)

        reviews = self.client.get(f"/djangoapp/reviews/dealer/{dealer_id}").json()
        self.assertEqual(reviews["status"], 200)

    def test_car_and_sentiment_endpoints(self):
        cars = self.client.get("/djangoapp/get_cars").json()["CarModels"]
        self.assertEqual(cars[0]["CarMake"], "Toyota")
        sentiment = self.client.get("/djangoapp/analyze/Fantastic%20services").json()
        self.assertEqual(sentiment["sentiment"], "positive")
