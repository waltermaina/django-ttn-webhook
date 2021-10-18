from django.shortcuts import render
from django.http import JsonResponse
from rest_api import models
from rest_api import serializers

def home(request):
    return render(request, 'home.html')

def humidity(request):
    return render(request, 'humidity.html')

def about(request):
    return render(request, 'about.html')

def contact_us(request):
    return render(request, 'contactus.html')

def pressure(request):
    return render(request, 'pressure.html')

def air_quality(request):
    return render(request, 'air_quality.html')

def temperature_chart(request):
    labels = []
    data = []
    # Get the last n records
    queryset = models.EnvironmentData.objects.all().order_by('-time_recorded')[:24]
    # Sort them in ascending order
    queryset = reversed(queryset)
    # There was a need to serilize the data
    serializer = serializers.EnvironmentDataSerializer(queryset, many=True)
    for entry in serializer.data:
        time_rec = entry['time_recorded']
        tim_rec_no_time_zone = time_rec.replace(":00+03:00","")
        labels.append(tim_rec_no_time_zone)
        #labels.append(entry['time'])
        data.append(entry['temperature'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def humidity_chart(request):
    labels = []
    data = []
    # Get the last n records
    queryset = models.EnvironmentData.objects.all().order_by('-time_recorded')[:24]
    # Sort them in ascending order
    queryset = reversed(queryset)
    # There was a need to serilize the data
    serializer = serializers.EnvironmentDataSerializer(queryset, many=True)
    for entry in serializer.data:
        time_rec = entry['time_recorded']
        tim_rec_no_time_zone = time_rec.replace(":00+03:00","")
        labels.append(tim_rec_no_time_zone)
        #labels.append(entry['time'])
        data.append(entry['humidity'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def pressure_chart(request):
    labels = []
    data = []
    # Get the last n records
    queryset = models.EnvironmentData.objects.all().order_by('-time_recorded')[:24]
    # Sort them in ascending order
    queryset = reversed(queryset)
    # There was a need to serilize the data
    serializer = serializers.EnvironmentDataSerializer(queryset, many=True)
    for entry in serializer.data:
        time_rec = entry['time_recorded']
        tim_rec_no_time_zone = time_rec.replace(":00+03:00","")
        labels.append(tim_rec_no_time_zone)
        #labels.append(entry['time'])
        data.append(entry['pressure'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def air_quality_chart(request):
    labels = []
    data = []
    # Get the last n records
    queryset = models.EnvironmentData.objects.all().order_by('-time_recorded')[:24]
    # Sort them in ascending order
    queryset = reversed(queryset)
    # There was a need to serilize the data
    serializer = serializers.EnvironmentDataSerializer(queryset, many=True)
    for entry in serializer.data:
        time_rec = entry['time_recorded']
        tim_rec_no_time_zone = time_rec.replace(":00+03:00","")
        labels.append(tim_rec_no_time_zone)
        #labels.append(entry['time'])
        data.append(entry['gas_resistance'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
