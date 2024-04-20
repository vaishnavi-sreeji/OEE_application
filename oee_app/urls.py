from django.contrib import admin
from django.urls import path
from . import views
from .views import add_production ,add_machine

urlpatterns = [
    path('admin/', admin.site.urls),
    path('oee/', views.get_oee, name='get_oee'),
    path('add_production/', views.add_production, name='add_production'),
    path('add_machine/', views.add_machine, name='add_machine')
]