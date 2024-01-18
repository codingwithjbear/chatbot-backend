from rest_framework.views import APIView
from rest_framework.response import Response
from openai import OpenAI

client = OpenAI()

class ChatGPTView(APIView):
    def post(self, request, *args, **kwargs):
        initial_conversation = [
            {"role": "system", "content": "You are an assistant for a store owner."},
            {"role": "assistant", "content": "Hello! How can I assist you with the store's inventory and onboarding?"},
            {"role": "assistant", "content": "Here is the current inventory list:"},
            {"role": "assistant", "content": "- Item 1: Description 1"},
            {"role": "assistant", "content": "- Item 2: Description 2"},
            {"role": "assistant", "content": "- Item 3: Description 3"},
            {"role": "assistant", "content": "And here are the onboarding documents:"},
            {"role": "assistant", "content": "1. Welcome Guide"},
            {"role": "assistant", "content": "2. Store Policies"},
            {"role": "assistant", "content": "3. Employee Handbook"},
        ]

        user_input = request.data.get('user_message')
        conversation = initial_conversation + [{"role": "user", "content": user_input}]

        if not user_input:
            return Response({'error': 'user_message field is required.'}, status=400)

        try:
            # Call to OpenAI's API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=conversation
            )

            # Extracting the response content
            openai_response = response.choices[0].message.content

            # Return the response
            return Response({'response': openai_response})

        except Exception as e:
            # Handle exceptions (e.g., API errors, network issues)
            return Response({'error': str(e)}, status=500)
