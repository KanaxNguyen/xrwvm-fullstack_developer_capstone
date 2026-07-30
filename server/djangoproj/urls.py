from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from djangoapp import views as djangoapp_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),
    path('fetchDealers', djangoapp_views.get_dealerships, name='fetch_dealers'),
    path('fetchDealers/<str:state>', djangoapp_views.get_dealerships, name='fetch_dealers_by_state'),
    path('fetchDealer/<int:dealer_id>', djangoapp_views.get_dealer_details, name='fetch_dealer_details'),
    path('fetchReviews/dealer/<int:dealer_id>', djangoapp_views.get_dealer_reviews, name='fetch_dealer_reviews'),
    path('', TemplateView.as_view(template_name="index.html")),
    path('about/', TemplateView.as_view(template_name="About.html")),
    path('contact/', TemplateView.as_view(template_name="Contact.html")),
    re_path(r'^login/?$', TemplateView.as_view(template_name="index.html")),
    re_path(r'^register/?$', TemplateView.as_view(template_name="index.html")),
    re_path(r'^dealers(?:/(?P<state>[^/]+))?/?$', TemplateView.as_view(template_name="index.html")),
    re_path(r'^dealer/(?P<id>\d+)/?$', TemplateView.as_view(template_name="index.html")),
    re_path(r'^postreview/(?P<id>\d+)/?$', TemplateView.as_view(template_name="index.html")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
