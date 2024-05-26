from django.urls import path
from .views import fetch_csv_data, mailer
urlpatterns = [
    path('mailer/', mailer, name='mailer'),
    path('fetch-csv-data/', fetch_csv_data, name='fetch-csv-data'),
]   