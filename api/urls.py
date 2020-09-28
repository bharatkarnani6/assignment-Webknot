from django.contrib import admin
from django.contrib.auth import views
from django.urls import path,include
from api import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
#router.register('hello-viewset',views.HelloViewSet,basename='hello-viewset')
router.register('users',views.UserProfileViewSet)

urlpatterns = [
   # path('hello-view/',views.HelloApiView.as_view()),
    path('api-token-auth/',views.UserLoginApiView.as_view(),name='auth-token'),
    path('signup/', views.RegisterAPI.as_view(), name='register'),
    path('change-password/',views.ChangePasswordView.as_view(), name='change-password'),
    path('reset-password/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('',include(router.urls)),
    
]
