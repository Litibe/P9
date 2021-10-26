"""Review_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'review'
urlpatterns = [
    path('home', views.home, name='home'),
    path('create_new_review', views.create_new_review, name='create_new_review'),
    path('create_new_ticket', views.create_new_ticket, name='create_new_ticket'),
    path('create_new_review_for_ticket/<int:number_ticket>',
         views.create_new_review_for_ticket, name='create_new_review_for_ticket'),
    path('create_new_ticket_and_review',
         views.create_new_ticket_and_review, name='create_new_ticket_and_review'),

    path('delete_ticket/<int:number_ticket>',
         views.delete_ticket, name='delete_ticket'),
    path('modify_ticket/<int:number_ticket>',
         views.modify_ticket, name='modify_ticket'),
    path('ticket/<int:number_ticket>', views.read_ticket, name='read_ticket'),

    path('delete_review/<int:number_review>',
         views.delete_review, name='delete_review'),
    path('modify_review/<int:number_review>',
         views.modify_review, name='modify_review'),

    path('flux', views.flux, name='flux'),
    path('posts', views.posts, name='posts'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
