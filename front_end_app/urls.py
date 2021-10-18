# front_end_app/urls.py
from django.urls import path
from .views import temperature_chart, home, humidity_chart, humidity, pressure, air_quality, about, contact_us, pressure_chart, air_quality_chart

urlpatterns = [
path('', home, name='home'),
path('humidity/', humidity, name='humidity'),
path('pressure/', pressure, name='pressure'),
path('air_quality/', air_quality, name='air_quality'),
path('about/', about, name='about'),
path('contactus/', contact_us, name='contactus'),
path('temperature_chart/', temperature_chart, name='temperature_chart'),
path('humidity_chart/', humidity_chart, name='humidity_chart'),
path('pressure_chart/', pressure_chart, name='pressure_chart'),
path('air_quality_chart/', air_quality_chart, name='air_quality_chart'),
]