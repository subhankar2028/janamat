from django.contrib.auth.models import User, Group
from jmat.models import *
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from rest_framework import serializers
from django.contrib.auth.models import User

# from rest_framework import serializers.ModelSerializer
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    # password = serializers.CharField(min_length=8)
    password = serializers.CharField(min_length=8, write_only=True)
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class TimelineSerializer(serializers.HyperlinkedModelSerializer):
# class TimelineSerializer(ModelSerializer):
    class Meta:
        model = Timeline
        fields = ['user', 'date_time', 'news_header', 'news']



# class Profile_Serializer(serializers.HyperlinkedModelSerializer):
class Profile_Serializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'profile_image', 'phone', 'dob', 'address', 'country', 'city', 'postal_code', ]






class Chellange_ListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chellange
        fields = ['id', 'ChellangeName', 'ChellangeDesc', 'created_on',]
    

class TopicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TopicList
        fields = ['id', 'Chellange_id', 'Topic', 'TopicDesc', 'voteCount', 'created_on',]
               

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ['Chellange_id', 'user_id', 'message', 'created_on', 'edit_Session_Expiry', ]


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vote
        fields = ['Chellange_id', 'Topic_id', 'User_id', 'is_votted',]
               
