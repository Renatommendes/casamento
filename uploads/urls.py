from django.urls import path
from .views import upload_view
from . import views



urlpatterns = [
     path('upload/', views.upload_view, name='upload_form'),
    
]
