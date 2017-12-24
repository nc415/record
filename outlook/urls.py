from django.conf.urls import url 
from outlook import views 

urlpatterns = [
  # The home view ('/outlook/') 
  url(r'^$', views.home, name='home'), 
  # Explicit home ('/outlook/home/') 
  url(r'^home/$', views.home, name='home'), 
  # Redirect to get token ('/outlook/gettoken/')
  url(r'^gettoken/$', views.gettoken, name='gettoken'),
  url(r'^mail/$', views.mail, name='mail'),
  url(r'^events/$', views.events, name='events')
]