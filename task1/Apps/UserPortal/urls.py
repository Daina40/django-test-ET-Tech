from django.urls import path
from Apps.UserPortal.views import *

urlpatterns = [
    path('api/v1/registration/', Registration.as_view(), name="registration"),
    path('api/v1/signin/', Signin.as_view(), name="signin")
]