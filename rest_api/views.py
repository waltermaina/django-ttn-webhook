# rest_api/views.py
from rest_framework import generics
from . import models
from . import serializers
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime
import requests
import json

HTTP_400_BAD_REQUEST = "NDAw"
HTTP_201_CREATED = "MjAx"

def queue_downlink_acknowledgement(status_code):
    """
        Sends a downlink message to the device as a way of
        acknowledging that data was received by the webhook.
    """
    
    url = 'https://eu1.cloud.thethings.network/api/v3/as/applications/ttn-webhook-application/webhooks/heroku-ttn-webhook/devices/eui-70b3d57ed00466e5/down/push'
    body = {
        "downlinks": [
            {
                "frm_payload": status_code,
                "f_port": 15,
                "priority": "NORMAL"
            }
        ]
    }

    headers = {'Authorization': 'Bearer NNSXS.DATPDITZQ6N5D7S6NSJSKC7YH4V7L6MRLGXCL4Y.AJP3JREGMCZULKKZOWRJZPUTUW4FCCJAQVOKELXCQEDQN3IAVQCA',
               'content-type': 'application/json',
               'User-Agent': 'heroku-ttn-webhook/1.0.0'
              }

    r = requests.post(url, data=json.dumps(body), headers=headers)

    print("Downlink Message Queue Response: ", r)

class ListData(APIView):
    """
        List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
    	queryset = models.EnvironmentData.objects.all()
    	serializer = serializers.EnvironmentDataSerializer(queryset, many=True)
    	return Response(serializer.data)

    def post(self, request, format=None):
        # extract data from TTN JSON object
        ttn_webhook_data = request.data
        print("ttn_webhook_data: ",ttn_webhook_data)

        # Check if it is uplink data
        if "decoded_payload" in str(ttn_webhook_data):
            raw_uplink_data = ttn_webhook_data
            uplink_message = raw_uplink_data["uplink_message"]
            #print(uplink_message)
            decoded_payload = uplink_message["decoded_payload"]
            #print(decoded_payload)
            decoded_payload_data = decoded_payload["data"]
            #print(decoded_payload_data)

            decoded_payload_errors = decoded_payload["errors"]
            decoded_payload_warnings = decoded_payload["warnings"]

            # Return if there is error in data
            if(decoded_payload_errors):
                queue_downlink_acknowledgement(HTTP_400_BAD_REQUEST)
                message = decoded_payload_errors[0]
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

            # Convert received time from milliseconds to datetime format
            time_milliseconds = decoded_payload_data['time_recorded']
            old_time = datetime.datetime.now().replace(microsecond=0)
            new_time = old_time - datetime.timedelta(milliseconds=int(time_milliseconds))
            decoded_payload_data['time_recorded'] = new_time.strftime("%Y-%m-%d %H:%M")

            # Change record_id to record's year, month, day and hour
            year = new_time.year
            month = new_time.month
            day = new_time.day
            hour = new_time.hour
            new_record_id = str(year)+str(month)+str(day)+str(hour)
            decoded_payload_data['record_id'] = int(new_record_id)
            print("Record ID: ", decoded_payload_data['record_id'])
            #print("Record: ", decoded_payload_data)

            # Save record and send a response    
            serializer = serializers.EnvironmentDataSerializer(data=decoded_payload_data)
            if serializer.is_valid():
                serializer.save()
                queue_downlink_acknowledgement(HTTP_201_CREATED)
                return Response(serializer.data, status=status.HTTP_201_CREATED) 
            queue_downlink_acknowledgement(HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            queue_downlink_acknowledgement(HTTP_400_BAD_REQUEST)
            message = "Incorrect json object received."
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

class LastRecordData(APIView):
    """
        Get the last record in db.
    """
    def get(self, request, format=None):
        last_record = models.EnvironmentData.objects.last()
        # If there are no records set record id to zero
        if last_record is None:
            last_record = models.EnvironmentData()
            last_record.record_id=0
        serializer = serializers.EnvironmentDataSerializer(last_record)
        return Response(serializer.data)


class DataDetail(APIView):
    """
        Retrieve, update or delete a data instance.
    """
    def get_object(self, pk):
        try:
            return models.EnvironmentData.objects.get(pk=pk)
        except models.EnvironmentData.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = serializers.EnvironmentDataSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = serializers.EnvironmentDataSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
