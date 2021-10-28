from django.db import models

class Advisor(models.Model):
    advisor_name = models.CharField(max_length=255)
    advisor_img_url = models.CharField(max_length=1000)

    def __str__(self):
        return self.advisor_name


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Booking(models.Model):
    booking_time = models.CharField(max_length=100)
    booking_user = models.CharField(max_length=100)
    booking_advisor = models.CharField(max_length=100)


    def __str__(self):
        return self.booking_time