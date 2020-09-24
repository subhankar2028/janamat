from rest_framework import generics
from django.contrib.auth.models import User, Group
from jmat.models import *
from rest_framework import viewsets
from . serializers import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from . pagination import LargeResultsSetPagination, StandardResultsSetPagination


#login api
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

#Register api
from rest_framework import generics, permissions
from rest_framework.response import Response
import knox
from knox.models import AuthToken
from rest_framework import status

#change password
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated   

#custom Permission ReadOnly
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

#Accet vote
from django.db.models import F

#Comment_PUT
from rest_framework import mixins
from rest_framework import generics

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

# Register API
# class RegisterAPI(generics.GenericAPIView):
#     """
#     An endpoint for register new user.
#     """
#     serializer_class = RegisterSerializer
#     def post(self, request, format='json'):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             if user:
#                 token = AuthToken.objects.create(user)[1]
#                 json = serializer.data
#                 return Response({
#                 "user": RegisterSerializer(user, context=self.get_serializer_context()).data,
#                 "token": AuthToken.objects.create(user)[1]
#                 })
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer

# Register API
class RegisterAPI(generics.GenericAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, knox.auth.TokenAuthentication]
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # print(request.data.user.id)
                # user = User.objects.get(username=str(request.user))
        print(User.objects.get(id = user.id))
        profile = UserProfile(user = User.objects.get(id = user.id), profile_image = 'na', phone = 'na', address = 'na', country = 'na', city = 'na', postal_code = 'na',)
        profile.save()

        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })




class LoginAPI(KnoxLoginView):
    """
    An endpoint for user login.
    """
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = [SessionAuthentication, BasicAuthentication, knox.auth.TokenAuthentication]
    # authentication_classes = [SessionAuthentication, BasicAuthentication, knox.auth.TokenAuthentication]
    serializer_class = ChangePasswordSerializer
    model = User
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
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


# class Update_profilej(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView,):
#     # queryset = UserProfile.objects.all()
#     # serializer_class = profile_Serializer
#     # permission_classes = [IsAuthenticated]
#     # authentication_classes = [SessionAuthentication, BasicAuthentication, knox.auth.TokenAuthentication]
#     # def get(self, request, *args, **kwargs):
#     #     return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         try:    
#             profile = UserProfile.objects.get(user_id = self.request.user.id)
#         except: return Response("Invalid comment")

#     def patch(self, request, *args, **kwargs):
#         return self.partial_update(request, *args, **kwargs)




class Timeline_List(viewsets.ModelViewSet):
# class Timeline_List(generics.ListCreateAPIView):
    """
    An endpoint for showing a the timeline.
    """
    permission_classes = [ReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication, knox.auth.TokenAuthentication]
    queryset = Timeline.objects.all().order_by('-date_time')
    serializer_class = TimelineSerializer
    pagination_class = StandardResultsSetPagination

# class Timeline_Update(viewsets.ModelViewSet):
class Timeline_Update(generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint for posting on timeline.
    """
    queryset = Timeline.objects.all().order_by('-date_time')
    serializer_class = TimelineSerializer
    # authentication_classes = [knox.auth.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, knox.auth.TokenAuthentication]

class Chellange_List(viewsets.ModelViewSet):
# class Chellange_List(generics.ListCreateAPIView):
    """
    An endpoint to get list of challenge.
    """
    permission_classes = [ReadOnly]
    queryset = Chellange.objects.all().order_by('-created_on')
    serializer_class = Chellange_ListSerializer
    pagination_class = StandardResultsSetPagination


# class Topic_List(viewsets.ModelViewSet):
class Topic_List(generics.ListAPIView):
    """
    An endpoint to get list of Topic.
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, knox.auth.TokenAuthentication]
    permission_classes = [ReadOnly]
    serializer_class = TopicSerializer
    def get_queryset(self):
        Chellange_id = self.kwargs['Chellange_id']
        return TopicList.objects.filter(Chellange_id=Chellange_id)


class Comment_List(generics.ListAPIView):
    """
    An endpoint to get list of Comment.
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, knox.auth.TokenAuthentication]
    permission_classes = [ReadOnly]
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination
    def get_queryset(self):
        # print(request.data)
        Chellange_id = self.kwargs['Chellange_id']
        return Comment.objects.filter(Chellange_id=Chellange_id)


class Comment_edit(  
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView,):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, knox.auth.TokenAuthentication]
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        try:    
            comment = Comment.objects.get(pk = kwargs['pk'], user_id = self.request.user.id)

            if timezone.now() > comment.edit_Session_Expiry:
                return Response("Edit session expired")       
            else:
                return self.update(request, *args, **kwargs)
        except: return Response("Invalid comment id")

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

# class Accept_Vote(viewsets.ModelViewSet):
class Accept_Vote(APIView):
    """
    An endpoint to get vote on a Topic.
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, knox.auth.TokenAuthentication]
    permission_classes = (IsAuthenticated,)             # <-- Knox Authentication(Defined in settings)
    def get(self, request, Topic_id):
        user = User.objects.get(username=str(request.user))
        try:
            try:
                topic = TopicList.objects.get(id=Topic_id)
            except:
                # return Response("invalid id")
                content = {
                    'username': str(request.user),
                    'Topic_id' : str(Topic_id),
                    'message' : 'Invalid request',
                }
                return Response(content)
            vote = Vote.objects.get(
            User_id=user.id, Chellange_id=topic.Chellange_id)
            content = {
                'username': str(request.user),
                'Topic_id' : str(Topic_id),
                'message' : 'You are already done the voting',
            }
            return Response(content)
        except:
            vote = Vote(Chellange_id=topic.Chellange_id,
                        Topic_id=Topic_id, User_id=user.id, is_votted=True)
            vote.save()
            TopicList.objects.filter(id=Topic_id).update(voteCount=F("voteCount") + 1)

            content = {
                'username': str(request.user),
                'Topic_id' : str(Topic_id),
                'message' : 'Your vote has accecpt',
            }
        return Response(content)


class contact_uss(APIView):
    """
    An endpoint to contact admin.
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, knox.auth.TokenAuthentication]
    def post(self, request, format = None):
        if request.method == 'POST':
            email = request.POST['email']
            mesg = request.POST['message']
            con_us = contact_us(email=email, message=mesg)
            con_us.save()
            content = {
                'greetigs'  : 'Thak you',
                'username'  : str(request.user), 
                'message'   : 'Your contact request has submitted successfully. We will get back to you soon',
            }
            return Response(content)


class Update_profile(  
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView,):
    queryset = UserProfile.objects.all()
    serializer_class = Profile_Serializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, knox.auth.TokenAuthentication]
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(user_id = request.user.id)
            return self.update(request, *args, **kwargs)
        except Exception as e:
            print(e) 
            return Response("Invalid profile id")

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # <-- Here
class HelloView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, knox.auth.TokenAuthentication]
    permission_classes = (IsAuthenticated,)             # <-- Knox Authentication(Defined in settings)
    def get(self, request, pk, format = None):
        content = {
            'username'  : str(request.user), 
            'message'   : 'Hello, World!',
            'primaryKey': str(pk),
            }
        return Response(content)


