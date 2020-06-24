from django.contrib import admin
from django.urls import path
from .views import GalleryView
urlpatterns = [
    path('<slug:slug>', GalleryView.as_view(), name="gallery")

]
