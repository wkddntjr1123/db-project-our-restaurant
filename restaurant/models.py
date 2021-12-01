from django.core import validators
from django.db import models
from django.db.models.deletion import CASCADE
from authentication.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    menus = models.CharField(max_length=100, blank=True, null=False, default="")
    phone = models.CharField(max_length=15, blank=True, null=False, default="")
    roadAddr = models.CharField(max_length=100)
    numberAddr = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        db_table = "restaurent"


# 평가 : user연결, restaurant연결
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=CASCADE)
    writer = models.ForeignKey(User, on_delete=CASCADE)
    contents = models.CharField(max_length=400)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "comment"
