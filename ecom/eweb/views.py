#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from eweb.models import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import RequestContext
# Create your views here.


@csrf_exempt
def homepage(request):
    """
    进入商城主页面 
    """
    return render(request, 'homepage.html')
