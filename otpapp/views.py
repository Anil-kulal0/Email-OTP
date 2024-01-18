from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  # Import status module for HTTP status codes

from .serializers import *
from .emails import send_otp_via_email

class RegisterApp(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                send_otp_via_email(serializer.data['email'])
                
                return Response({
                    'message': 'Registration successful, check email',
                    'data': serializer.data,
                }, status=status.HTTP_200_OK)

            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Registration failed',
                'data': serializer.errors
            })

        except Exception as e:
            # Handle specific exceptions if needed
            print(e)
            return Response({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Internal Server Error',
            })
class verifyOTP(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyAccountSerializer(data = data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']
                
                user =  User.objects.filter(email = email)
                if not user.exists():
                    return Response({
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'Something went wrong',
                        'data': 'invalid email'
                    })
                    
                if user[0].otp != otp:
                    return Response({
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'Something went wrong',
                        'data': 'Wrong otp'
                    })
                user = user.first()    
                user.is_verified = True
                user.save()    
                        
                
                return Response({
                    'message': 'Account verified',
                    'data': {},
                    'status':200})

            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Registration failed',
                'data': serializer.errors
            })
            
        except Exception as e:
            # Handle specific exceptions if needed
            print(e)
            return Response({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Internal Server Error',
            })