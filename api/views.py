from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets,filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from api import models
from api import serializers
from api import permission

from knox.models import AuthToken
from rest_framework import generics, permissions

from django.contrib.auth.models import User
from api.serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated  
#password=maheswari1@

# Create your views here.
# class HelloApiView(APIView):
#     serializer_class=serializers.HelloSerializer
#     def get(self,request,format=None):
#         an_apiview=[
#             'Uses Http methods as functions (get,post,patch,put,delete)'
#         ]
#         return Response({'message':'Hello!', 'an_apiview':an_apiview})

#     def post(self,request):
#         serializers=self.serializer_class(data=request.data)

#         if serializers.is_valid():
#             name=serializers.validated_data.get('name')
#             message=f'Hello {name}'
#             return Response({'message':message})
#         else:
#             return Response(
#                 serializers.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#                 )

#     def put(self, request, pk=None):
#         return Response({'method':'PUT'})

#     def patch(self, request, pk=None):
#         return Response({'method':'PATCH'})
    
#     def delete(self, request, pk=None):
#         return Response({'method':'DELETE'})
    
# class HelloViewSet(viewsets.ViewSet):
#     def list(self,request):
#         a_viewset=[
#             'Uses actions'
#         ]
#         return Response({'message':'Hello','a_viewset':a_viewset})

    

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class=serializers.UserProfileSerializer
    queryset=models.UserProfile.objects.all()
    authentication_classes=(TokenAuthentication,)
    permission_classes=(permission.UpdateOwnProfile,)
    filter_backends=(filters.SearchFilter,)
    search_fields=('name','email')


class UserLoginApiView(ObtainAuthToken):
    renderer_classes=api_settings.DEFAULT_RENDERER_CLASSES

class RegisterAPI(generics.GenericAPIView):
    serializer_class = serializers.UserProfileSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        # "user": UserProfileSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

class ChangePasswordView(generics.UpdateAPIView):
    
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)