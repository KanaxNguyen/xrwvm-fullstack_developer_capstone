import json
import logging
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .restapis import analyze_review_sentiments, get_request, post_review

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    data = json.loads(request.body or "{}")
    username = data.get('userName', '')
    password = data.get('password', '')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({
            "userName": username,
            "firstName": user.first_name,
            "lastName": user.last_name,
            "status": "Authenticated",
        })
    return JsonResponse({"userName": username, "status": "Failed"}, status=401)


def logout_request(request):
    logout(request)
    return JsonResponse({"userName": "", "status": "Logged out"})


@csrf_exempt
def registration(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    data = json.loads(request.body or "{}")
    username = data.get('userName')
    password = data.get('password')
    first_name = data.get('firstName', '')
    last_name = data.get('lastName', '')
    email = data.get('email', '')
    if not username or not password:
        return JsonResponse({"error": "Username and password are required"}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({"userName": username, "error": "Already Registered"})
    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email,
    )
    login(request, user)
    return JsonResponse({
        "userName": username,
        "firstName": first_name,
        "lastName": last_name,
        "status": "Authenticated",
    })


def get_dealerships(request, state="All"):
    if state == "All":
        dealerships = get_request("/fetchDealers")
    else:
        dealerships = get_request(f"/fetchDealers/{state}")
    if request.path.startswith('/fetchDealers'):
        return JsonResponse(dealerships, safe=False)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    reviews = get_request(f"/fetchReviews/dealer/{dealer_id}")
    for review in reviews:
        sentiment = analyze_review_sentiments(review.get("review", ""))
        review["sentiment"] = sentiment.get("sentiment", sentiment.get("label", "neutral"))
    if request.path.startswith('/fetchReviews'):
        return JsonResponse(reviews, safe=False)
    return JsonResponse({"status": 200, "reviews": reviews})


def get_dealer_details(request, dealer_id):
    dealer = get_request(f"/fetchDealer/{dealer_id}")
    if request.path.startswith('/fetchDealer'):
        return JsonResponse(dealer, safe=False)
    return JsonResponse({"status": 200, "dealer": dealer})


@csrf_exempt
def add_review(request):
    data = json.loads(request.body)
    data["name"] = request.user.username if request.user.is_authenticated else data.get("name", "anonymous")
    result = post_review(data)
    return JsonResponse({"status": 200, "review": result})


def get_cars(request):
    car_models = []
    for car_model in CarModel.objects.select_related("car_make").all():
        car_models.append({
            "CarMake": car_model.car_make.name,
            "CarModel": car_model.name,
        })
    if len(car_models) < 15:
        demo_cars = [
            {"CarMake": "Toyota", "CarModel": "Camry"},
            {"CarMake": "Toyota", "CarModel": "Corolla"},
            {"CarMake": "Toyota", "CarModel": "RAV4"},
            {"CarMake": "Honda", "CarModel": "Civic"},
            {"CarMake": "Honda", "CarModel": "Accord"},
            {"CarMake": "Honda", "CarModel": "CR-V"},
            {"CarMake": "Ford", "CarModel": "F-150"},
            {"CarMake": "Ford", "CarModel": "Mustang"},
            {"CarMake": "Ford", "CarModel": "Explorer"},
            {"CarMake": "Tesla", "CarModel": "Model 3"},
            {"CarMake": "Tesla", "CarModel": "Model Y"},
            {"CarMake": "BMW", "CarModel": "3 Series"},
            {"CarMake": "BMW", "CarModel": "X5"},
            {"CarMake": "Chevrolet", "CarModel": "Silverado"},
            {"CarMake": "Nissan", "CarModel": "Altima"},
        ]
        return JsonResponse({"CarModels": demo_cars})
    return JsonResponse({"CarModels": car_models})


def analyze_review(request, text):
    result = analyze_review_sentiments(text)
    return JsonResponse({"text": text, **result})
