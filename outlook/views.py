from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from outlook.authhelper import get_signin_url, get_token_from_code, get_access_token
from outlook.outlookservice import get_me, get_my_messages, get_my_events
import time
import datetime

# Create your views here.

def home(request):
	redirect_uri = request.build_absolute_uri(reverse('outlook:gettoken'))
	sign_in_url = get_signin_url(redirect_uri)
	return HttpResponse('<a href="' + sign_in_url +'">Click here to sign in and view your mail</a>')

def gettoken(request):

	auth_code=request.GET['code']
	redirect_uri=request.build_absolute_uri(reverse('outlook:gettoken'))
	token=get_token_from_code(auth_code,redirect_uri)
	access_token=token['access_token']
	user=get_me(access_token)
	refresh_token=token['refresh_token']
	expires_in=token['expires_in']

	#expires in is in seconds
	#get current timestamp and add expires in to get expiration time
	#subtract 5 mins to allow for clock differences

	expiration=int(time.time())+expires_in-300

	# save the token in the session
	request.session['access_token']=access_token
	request.session['refresh_token']=refresh_token
	request.session['token_expires']=expiration
	request.session['user_email']=user['mail']

	return HttpResponseRedirect(reverse('outlook:mail'))

def mail(request):
	access_token=get_access_token(request, request.build_absolute_uri(reverse('outlook:gettoken')))
	user_email=request.session['user_email']
	#If there is no token in the session then redirect to home
	if not access_token:
		return HttpResponseRedirect(reverse('tutorial:home'))
	else:
		messages=get_my_messages(access_token,user_email)
		context = {'messages':messages['value']}
		return render(request, 'outlook/mail.html', context)

def events(request):
	access_token=get_access_token(request, request.build_absolute_uri(reverse('outlook:gettoken')))
	user_email=request.session['user_email']
	#if no access token return to home
	if not access_token:
		return HttpResponseRedirect(reverse('outlook:home'))
	else:
		events=get_my_events(access_token,user_email)
		'''#dt=datetime.date.now()
		#current_datettime=datetime.strptime(dt, "%Y-%m-%d")

		now = datetime.datetime.now() 
		print(now)
		#print(current_datettime)
		for event in events:
			if 'dateTime'> '2015':
				print("yay")
			else:
				pass'''

		context ={'events':events['value']}
		return render(request, 'outlook/events.html', context)
