from django.urls import path
from . import views

urlpatterns = [
    path('admin/advisor/', views.AdminView.as_view()),
    path('user/register/', views.UserRegister.as_view()),
    path('user/login/', views.UserLogin.as_view()),
    path('user/<int:user_id>/advisor/', views.GetAllAdvisors.as_view()),
    path('user/<int:user_id>/advisor/<int:advisor_id>/', views.BookAdvisor.as_view()),
    path('user/<int:user_id>/advisor/booking/', views.GetAllBookedCall.as_view()),
]