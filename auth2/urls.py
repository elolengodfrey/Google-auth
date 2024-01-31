from django.urls import path
from auth2.views import *

urlpatterns = [
    path('', SignInView.as_view(), name='sign_in'),
    path('sign-out', SignOutView.as_view(), name='sign_out'),
    path('auth-receiver', Home.as_view(), name='accounts'),
]

