from django.contrib import admin
from django.urls import path, include
from uploads import views 
from uploads.views import upload_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', upload_view, name='home'),  # <- Aqui está a rota da raiz
    path('upload/', upload_view, name='upload'),
    path('upload/', include('uploads.urls')),  # Isso é obrigatório
]