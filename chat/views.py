from rest_framework.views import APIView
from rest_framework.response import Response
from openai import OpenAI
import json

client = OpenAI()

class ChatGPTView(APIView):
    def post(self, request, *args, **kwargs):

        store1_inventory = {
            "store_name": "Deerbrook Mall Store",
            "store_number": 103,
            "location": "123 Deerbrook Mall, Cityville",
            "inventory": [
                {
                    "product_id": "SHOE001",
                    "product_name": "Men's Running Shoes",
                    "brand": "Nike",
                    "size": "10",
                    "color": "Black/White",
                    "price": "$89.99",
                    "quantity": 25
                },
                {
                    "product_id": "SHOE002",
                    "product_name": "Women's Sneakers",
                    "brand": "Adidas",
                    "size": "8",
                    "color": "Pink/Grey",
                    "price": "$69.99",
                    "quantity": 15
                }
            ]
        }

        store2_inventory = {
            "store_name": "The Woodlands Mall",
            "store_number": 104,
            "location": "456 Oak Avenue, Woodlands Town",
            "inventory": [
                {
                    "product_id": "SHOE001",
                    "product_name": "Men's Running Shoes",
                    "brand": "Hoka",
                    "size": "10",
                    "color": "Black",
                    "price": "$189.99",
                    "quantity": 54
                },
                {
                    "product_id": "SHOE002",
                    "product_name": "Women's Sneakers",
                    "brand": "Adidas",
                    "size": "8",
                    "color": "Pink/Grey",
                    "price": "$69.99",
                    "quantity": 33
                },
                {
                    "product_id": "SHOE003",
                    "product_name": "Air Force 1",
                    "brand": "Nike",
                    "size": "13",
                    "color": "White",
                    "price": "$99.99",
                    "quantity": 65
                },
                {
                    "product_id": "SHOE004",
                    "product_name": "Jordans",
                    "brand": "Nike",
                    "size": "12",
                    "color": "Green",
                    "price": "$129.99",
                    "quantity": 34
                }
            ]
        }

        onboarding_doc = {
            "title": "Employee Handbook",
            "content": "Welcome to the team! This handbook contains all you need to know..."
        }

        store1 = json.dumps(store1_inventory)
        store2 = json.dumps(store2_inventory)

        user_input = request.data.get('user_message')

        if not user_input:
            return Response({'error': 'user_message field is required.'}, status=400)
        
        #mock onboarding doc response (to make this real we'd need to have a path to these documents)
        if 'onboarding' in user_input.lower():
            return Response({'onboarding_document': onboarding_doc})
        
        #mock clock in/out responses (to make this work we'd need to connect this to a database and sync with employeeid...)
        clock_in_phrases = ['clock in', 'clock me in', 'start my shift', 'begin my workday']
        clock_out_phrases = ['clock out', 'clock me out', 'end my shift', 'done for the day']
        if any(phrase in user_input.lower() for phrase in clock_in_phrases):
            return Response({'response': 'You have been successfully clocked in!'})
        if any(phrase in user_input.lower() for phrase in clock_out_phrases):
            return Response({'response': 'You have been successfully clocked out!'})

        #for everything else go through GPT 
        conversation = [
            {"role": "system", "content": "You are a virtual assistant for Finish Line shoe stores Employees."},
            {"role": "assistant", "content": "You are being used at The Woodlands Mall location."},
            {"role": "assistant", "content": "Hello! How can I assist you with our shoe stores' inventory?"},
            {"role": "assistant", "content": "Deerbrook Mall Store Inventory:"},
            {"role": "assistant", "content": store1},
            {"role": "assistant", "content": "The Woodlands Mall Inventory:"},
            {"role": "assistant", "content": store2},
            {"role": "assistant", "content": "You are employeed at The Woodlands Mall Location."},
            {"role": "assistant", "content": "This is how you open the store according to the employee handbook..."},
            {"role": "assistant", "content": "This is how you close the store according to the employee handbook..."},
            {"role": "user", "content": user_input},
        ]

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=conversation
            )

            openai_response = response.choices[0].message.content

            return Response({'response': openai_response})

        except Exception as e:
            # Handle exceptions
            return Response({'error': str(e)}, status=500)
