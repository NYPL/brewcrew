import datetime
from pdb import set_trace

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render

from oauth2client.client import flow_from_clientsecrets

from .models import (
    Credential,
    User,
)


FLOW = flow_from_clientsecrets(
    settings.GOOGLE_OAUTH_CLIENT_SECRETS,
    scope=[
        'https://www.googleapis.com/auth/calendar',
        'https://www.googleapis.com/auth/userinfo.email',
    ],
    redirect_uri='http://localhost:8000/accounts/google_callback',
)


def index(request):
    return render(
        request, 'accounts/register.html', {},
        content_type='text/html; charset=utf-8'
    )


def success(request):
    return render(
        request, 'accounts/register-success.html', {},
        content_type='text/html; charset=utf-8'
    )


def google_callback(request):
    error = request.GET.get('error')
    if error:
        raise ValueError('We gots prahblems.')

    code = request.GET.get('code')
    if not code:
        raise ValueError('No code returned')

    credentials = FLOW.step2_exchange(code)

    email = credentials.id_token.get('email')
    if not email:
        raise ValueError('No email provided.')

    user = User.objects.get(email=email)
    if not user:
        raise ValueError('No user found')

    expires_in = datetime.timedelta(seconds = int(credentials._expires_in() * 0.9))
    expires_at = datetime.datetime.utcnow() + expires_in

    credential = Credential(
        id=user, credential = credentials.to_json(), expires_at=expires_at
    )
    credential.save()
    return HttpResponse("Successfully registered.")

def register(request):
    email = request.POST.get('email')
    name = request.POST.get('name')

    if not (email and name):
        raise ValueError("Can't register without email and name")

    nickname = request.POST.get('nickname')
    location_only = (request.POST['match']=='near')
    description = request.POST.get('message')

    user = User(
        email=email, name=name, nickname=nickname,
        description=description, location_only=location_only,
    )
    user.save()

    authorization_url = FLOW.step1_get_authorize_url()
    return redirect(authorization_url)
