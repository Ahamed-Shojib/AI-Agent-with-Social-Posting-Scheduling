from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.designer_view, name='designer_view'),
    path('save/', views.save_customization, name='save_customization'),
]