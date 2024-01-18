from rest_framework import serializers

class ChatGPTSerializer(serializers.Serializer):
    user_message = serializers.CharField(max_length=1000)  # Example of input validation
    response = serializers.CharField(max_length=1000, required=False)  # For the OpenAI response
