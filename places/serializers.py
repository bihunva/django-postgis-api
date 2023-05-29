from django.contrib.gis.geos import Point
from rest_framework import serializers
from rest_framework_gis.serializers import GeoModelSerializer

from .models import Place


class PlaceSerializer(GeoModelSerializer):
    longitude = serializers.FloatField(write_only=True)
    latitude = serializers.FloatField(write_only=True)

    class Meta:
        model = Place
        fields = ("id", "name", "description", "geom", "longitude", "latitude")
        read_only_fields = ("id", "geom")

    @staticmethod
    def set_point_data(validated_data:  dict) -> dict:
        longitude = validated_data.pop("longitude")
        latitude = validated_data.pop("latitude")
        validated_data["geom"] = Point(longitude, latitude)
        return validated_data

    def create(self, validated_data) -> Place:
        return super().create(self.set_point_data(validated_data))

    def update(self, instance, validated_data) -> Place:
        return super().update(instance, self.set_point_data(validated_data))
