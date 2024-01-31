import os
import logging
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from google.oauth2 import id_token
from google.auth.transport import requests

class SignInView(View):
    def get(self, request):
        return render(request, 'home.html')

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class Home(View):
    def post(self, request):
        token = request.POST.get('credential', None)

        if not token:
            logger.error("No token received in the request.")
            return HttpResponse(status=400)

        try:
            user_data = id_token.verify_oauth2_token(
                token, requests.Request(), os.environ.get('GOOGLE_OAUTH_CLIENT_ID', '')
            )
        except ValueError as e:
            logger.error(f"Error verifying OAuth2 token: {e}")
            return HttpResponse(status=403)

        # In a real app, save any new user data to the database here.
        request.session['user_data'] = user_data

        return HttpResponseRedirect('/')

class SignOutView(View):
    def get(self, request):
        del request.session['user_data']
        return HttpResponseRedirect('/')
