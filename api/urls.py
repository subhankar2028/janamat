from django.urls import include, path
from django.conf.urls import url

from rest_framework import routers
from . import views
from knox import views as knox_views
from .views import LoginAPI
from rest_framework.authtoken.views import obtain_auth_token  # <-- Here

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'Timeline_List', views.Timeline_List)
# router.register(r'Timeline_Update/<int:pk>', views.Timeline_Update)
router.register(r'Chellange_List', views.Chellange_List)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('RegisterAPI/', views.RegisterAPI.as_view(), name='register'),
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('Update_profile/<int:pk>/', views.Update_profile.as_view()),

    # path('Timeline_List/', views.Timeline_List.as_view()),			
    path('Timeline_Update/<int:pk>/', views.Timeline_Update.as_view()),
    # path('Chellange_List/', views.Chellange_List.as_view()),		
    url('Topic_List/(?P<Chellange_id>.+)/$', views.Topic_List.as_view()),
    url('Comment_List/(?P<Chellange_id>.+)/$', views.Comment_List.as_view()),
    path('Comment_edit/<int:pk>/', views.Comment_edit.as_view()),

    path('Accept_Vote/<int:Topic_id>/', views.Accept_Vote.as_view(), name='Accept_Vote'),
    path('contact_uss/', views.contact_uss.as_view(), name='contact_uss'),
    path('hello/<int:pk>/', views.HelloView.as_view(), name='hello'),
]