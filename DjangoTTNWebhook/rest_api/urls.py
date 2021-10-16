# api_app/urls.py
from django.urls import include, path

from . import views

urlpatterns = [
    path('v1/', views.ListData.as_view()),
    path('v1/last/', views.LastRecordData.as_view()),
    path('v1/<str:pk>/', views.DataDetail.as_view()),
]