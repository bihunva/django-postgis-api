from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from .models import Place
from .serializers import PlaceSerializer

SRID = 4326


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "longitude",
                OpenApiTypes.FLOAT,
                description="Longitude of the reference point",
                required=False
            ),
            OpenApiParameter(
                "latitude",
                OpenApiTypes.FLOAT,
                description="Latitude of the reference point",
                required=False
            ),
        ]
    )
    def list(self, request, *args, **kwargs) -> Response:
        """
        Get the nearest place to the given coordinates if provided,
        otherwise return a list of places.
        """
        longitude = float(request.query_params.get("longitude", 0))
        latitude = float(request.query_params.get("latitude", 0))

        if longitude and latitude:
            reference_point = Point(longitude, latitude, srid=SRID)
            return self.find_nearest_place(reference_point)

        if longitude or latitude:
            raise ParseError("Please provide both longitude and latitude")

        return super().list(request, *args, **kwargs)

    def find_nearest_place(self, point: Point) -> Response:
        """
        Find the nearest place to the given reference point,
        returning a corresponding message if no place is found.
        """
        places = self.queryset.annotate(distance=Distance("geom", point))
        nearest_place = places.order_by("distance").first()

        if not nearest_place:
            return Response({"message": "No nearest place found."})

        return Response(self.get_serializer(nearest_place).data)
