from django.contrib.gis.geos import Point
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Place

PLACE_LIST_URL = "place-list"
PLACE_DETAIL_URL = "place-detail"


class PlaceTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.place1 = Place.objects.create(
            name="Place 1",
            description="Description 1",
            geom=Point(0, 0),
        )
        self.place2 = Place.objects.create(
            name="Place 2",
            description="Description 2",
            geom=Point(1, 1),
        )

    def test_create_place(self):
        url = reverse(PLACE_LIST_URL)
        data = {
            "name": "New Place",
            "description": "New Description",
            "longitude": 3,
            "latitude": 3,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Place.objects.count(), 3)

    def test_create_place_missing_coordinates(self):
        url = reverse(PLACE_LIST_URL)
        data = {
            "name": "New Place",
            "description": "New Description",
            "longitude": 3,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Place.objects.count(), 2)

    def test_retrieve_place(self):
        url = reverse(PLACE_DETAIL_URL, args=[self.place1.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Place 1")

    def test_list_places(self):
        url = reverse(PLACE_LIST_URL)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_nearest_place(self):
        url = reverse(PLACE_LIST_URL)
        response = self.client.get(url, {"longitude": 2, "latitude": 2})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Place 2")

    def test_delete_place(self):
        url = reverse(PLACE_DETAIL_URL, args=[self.place1.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Place.objects.count(), 1)
