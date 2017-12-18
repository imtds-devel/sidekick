"""sidekick URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from cas import views
from shifts.functions import sync
from .views import oauth_handler, oauth_test

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', RedirectView.as_view(url=('homebase/'))),
    url(r'^homebase/', include('homebase.urls')),
    url(r'^passwords/', include('passwords.urls')),
    url(r'^printinfo/', include('printinfo.urls')),
    url(r'^quotes/', include('quotes.urls')),
    url(r'^roster/', include('roster.urls')),
    url(r'^shifts/', include('shifts.urls')),
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^accounts/logout/$', views.logout, name='logout'),
    url(r'^google/synchronize/', sync.sync),
    url(r'^oauth2handler/', oauth_handler),
    url(r'^oauthtest/', oauth_test),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
