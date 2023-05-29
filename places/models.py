from django.contrib.gis.db import models


class Place(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    geom = models.PointField(help_text="The coordinates of the place")

    def __str__(self) -> str:
        return self.name

