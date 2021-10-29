from django.http.response import HttpResponse
from django.shortcuts import render

from .models import Advisor, User, Booking

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import jwt
from datetime import datetime, timedelta



class AdminView(APIView):
    def post(self, request, format=None):
        data = request.data

        name = data.get('advisor_name', "")
        img_url = data.get('advisor_photo_url', "")

        content = {}

        if(name == "" or img_url == ""):
            content["msg"] = "Error"
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            content["msg"] = "Success"

            advisor = Advisor(advisor_name=name, advisor_img_url=img_url)
            advisor.save()

            return Response(content, status=status.HTTP_200_OK)



class UserRegister(APIView):
    def post(self, request, format=None):
        data = request.data

        name = data.get('name', "")
        email = data.get('email', "")
        password = data.get('password', "")

        if(name == "" or email == "" or password == ""):
            return Response(None,status=status.HTTP_400_BAD_REQUEST)
        
        content = {}

        user = User(name=name, email=email, password=password)
        user.save()

        dt = datetime.now() + timedelta(days=2)           
        encoded_token = jwt.encode({'email': email, 'password': password, 'exp': dt }, settings.SECRET_KEY, algorithm='HS256')

        content['JWTAuth'] = encoded_token
        content['userid'] = user.id
        
        return Response(content, status=status.HTTP_200_OK)



class UserLogin(APIView):
    def post(self, request, format=None):
        data = request.data

        email = data.get('email', "")
        password = data.get('password', "")

        if(email == "" or password == ""):
            return Response(None,status=status.HTTP_400_BAD_REQUEST)

        user = None

        try:
            user = User.objects.get(email=email, password=password)
        except User.DoesNotExist:
            user = None

        content = {}

        if(user):
            dt = datetime.now() + timedelta(days=2)           
            encoded_token = jwt.encode({'email': email, 'password': password, 'exp': dt }, settings.SECRET_KEY, algorithm='HS256')
            content['JWTAuth'] = encoded_token
            content['userid'] = user.id
            return Response(content, status=status.HTTP_200_OK)
        else:
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)



class GetAllAdvisors(APIView):
    def get(self, request, user_id, format=None):
        advisors = Advisor.objects.all()

        res_arr = []

        for advisor in advisors:
            obj = {
                "Advisor Name": advisor.advisor_name,
                "Advisor Profile Pic": advisor.advisor_img_url,
                "Advisor Id": advisor.id
            }
            res_arr.append(obj)

        content = {
            "Advisors": res_arr
        }

        return Response(content, status=status.HTTP_200_OK)



class BookAdvisor(APIView):
    def post(self, request, user_id, advisor_id, format=None):
        user = None
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            user = None

        advisor = None
        try:
            advisor = Advisor.objects.get(id=advisor_id)
        except Advisor.DoesNotExist:
            advisor = None

        booking_time = request.data.get("booking_time", "")

        if(user and advisor and booking_time != ""):
            booking = Booking(booking_time=booking_time, booking_user=user_id, booking_advisor=advisor_id)
            booking.save()

            return Response(None, status=status.HTTP_200_OK)
        else:
            return Response(None,status=status.HTTP_400_BAD_REQUEST)
        


class GetAllBookedCall(APIView):
    def get(self, request, user_id, format=None):

        bookings = None
        try:
            bookings = Booking.objects.all().filter(booking_user=user_id)
        except Booking.DoesNotExist:
            bookings = None

        if(bookings is None):
            return Response(None,status=status.HTTP_400_BAD_REQUEST)
        
        res_arr = []

        for book in bookings:
            advisor = Advisor.objects.get(id=book.booking_advisor)
            obj = {
                "Advisor Name": advisor.advisor_name,
                "Advisor Profile Pic": advisor.advisor_img_url,
                "Advisor Id": advisor.id,
                "Booking time": book.booking_time,
                "Booking id": book.id
            }
            res_arr.append(obj)


        content = {
            "All Booked Calls" : res_arr
        }

        return Response(content, status=status.HTTP_200_OK)

