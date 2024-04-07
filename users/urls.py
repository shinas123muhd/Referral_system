from django.urls import path
from .views import RegisterUser,UserDetails,ViewReferrals


urlpatterns = [
    path('registeruser/',RegisterUser.as_view(),name='registeruser'),
    path('userdetails/<int:id>/',UserDetails.as_view(),name='userdetails'),
    path('viewreferrals/<int:id>/',ViewReferrals.as_view(),name='viewreferrals'),

]