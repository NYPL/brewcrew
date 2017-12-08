from pdb import set_trace
from django.http import HttpResponse
from django.shortcuts import redirect, render

from oauth2client.client import flow_from_clientsecrets


FLOW = flow_from_clientsecrets(
    'client_secrets.json',
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
    authorization_url = FLOW.step1_get_authorize_url()
    # return redirect(authorization_url)

def google_callback(request):
    error = request.GET.get('error')
    if error:
        raise ValueError('We gots prahblems.')

    code = request.GET.get('code')
    if not code:
        raise ValueError('No code returned')

    credentials = FLOW.step2_exchange(code)
    return HttpResponse("hey")
