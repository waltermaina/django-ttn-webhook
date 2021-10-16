# api_app/serializers.py
from rest_framework import serializers
from . import models


class EnvironmentDataSerializer(serializers.ModelSerializer):
    """
        A class that will manage serialization and 
        deserialization from JSON of EnvironmentData
        model's data.
    """
    class Meta:
        fields = (
            'record_id',
            'time_recorded',
            'temperature',
            'pressure',
            'humidity',
            'gas_resistance'
        )
        model = models.EnvironmentData