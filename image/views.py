from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import cloudinary.uploader

from .serializers import MediaUploadSerializer

class MediaUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MediaUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            file_type = file.content_type

            if file_type.startswith('image'):
                folder = 'image'
            elif file_type == 'application/pdf':
                folder = 'pdf'
            elif file_type.startswith('video'):
                folder = 'video'
            else:
                return Response({'error': 'Unsupported file type'}, status=status.HTTP_400_BAD_REQUEST)

            upload_result = cloudinary.uploader.upload(file, folder=folder)
            return Response({
                'message': 'Upload successful',
                'url': upload_result['url'],
                'type': folder
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
