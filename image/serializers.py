from rest_framework import serializers

class MediaUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        file_type = value.content_type
        file_size = value.size

        if file_type.startswith('image'):
            if file_size > 5 * 1024 * 1024:
                raise serializers.ValidationError("Image files must be less than 5MB")
        elif file_type == 'application/pdf':
            if file_size > 5 * 1024 * 1024:
                raise serializers.ValidationError("PDF files must be less than 5MB")
        elif file_type.startswith('video'):
            if file_size > 10 * 1024 * 1024:
                raise serializers.ValidationError("Video files must be less than 10MB")
        else:
            raise serializers.ValidationError("Unsupported file type")
        
        return value
