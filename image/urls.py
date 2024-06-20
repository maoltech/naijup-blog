from django.urls import path
from .views import MediaUploadView

urlpatterns = [
    path('', MediaUploadView.as_view(), name='media-upload'),
]
