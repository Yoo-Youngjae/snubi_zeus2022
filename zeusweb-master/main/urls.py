from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.main, name="main"),
    path("camera",views.camera, name="camera"), # logitec camera
    path("face",views.face, name="face"), # face camera
]