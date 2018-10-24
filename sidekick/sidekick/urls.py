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
from django.urls import include, path
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from cas import views
from .views import new_task, complete_task

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url=('homebase/'))),
    path('homebase/', include('homebase.urls')),
    path('passwords/', include('passwords.urls')),
    path('printinfo/', include('printinfo.urls')),
    path('quotes/', include('quotes.urls')),
    path('roster/', include('roster.urls')),
    path('shifts/', include('shifts.urls')),
    path('accounts/login/', views.login, name='login'),
    path('accounts/logout/', views.logout, name='logout'),
    path('ajax/newtask', new_task),
    path('ajax/completetask', complete_task)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
