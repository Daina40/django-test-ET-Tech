import os
import json
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Users
from .serializers import UserSerializer


class Registration(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # path of the JSON file
            project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            json_file_path = os.path.join(project_dir, 'UserPortal', 'user.json')
            
            try:
                # Load JSON data
                with open(json_file_path, 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                # to read empty list
                data = []

            # Check if the email already exists in the existing data
            email = serializer.validated_data['email']
            if any(user['email'] == email for user in data):
                return Response({"error": "Email address already exists."},
                                status=status.HTTP_400_BAD_REQUEST)

            # if email not exists than append the new data
            data.append(serializer.data)

            # Save the updated JSON data
            with open(json_file_path, 'w') as f:
                json.dump(data, f, indent=4)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Signin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        # required of email and password
        if not email or not password:
            return Response({"error": "Both email and password are required."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # credentials of email [email exists]
        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        
        # provided password matches the user's password
        if user.password == password:
            return Response({"message": "Authentication successful."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        
