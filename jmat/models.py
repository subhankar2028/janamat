from django.db import models
from django.contrib.auth.models import User
from datetime import *


USER_TYPE = (
    (1, "Admin"),
    (2, "User")
)

def hour_hence(h):
        return timezone.now() + timezone.timedelta(hours=h)


class UserProfile(models.Model):
    # This line binds this extended profile with user
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    profile_image = models.ImageField(
        upload_to="janamat/ProfileImage", blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    # dob = models.DateTimeField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)

    # usr_type = models.IntegerField(choices=USER_TYPE, default=2)
    address = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=6, blank=True, null=True)

    # def __str__(self):
    #     return str(self.user)
    class Meta:
        db_table = "UserProfile"

# class UserProfile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
#     title = models.CharField(max_length=5)
#     dob = models.DateField()
#     address = models.CharField(max_length=255)
#     country = models.CharField(max_length=50)
#     city = models.CharField(max_length=50)
#     zip = models.CharField(max_length=5)
#     photo = models.ImageField(upload_to='uploads', blank=True)




class Chellange(models.Model):
    ChellangeName = models.CharField(max_length=50, blank=False, null=False)
    ChellangeDesc = models.TextField(max_length=1000, blank=True, null=True)
    created_on = models.DateTimeField(auto_now=True )
    # created_on = models.DateTimeField(default=datetime.today)
    # topiclist = models.ForeignKey(TopicList, on_delete=models.CASCADE)

    def __str__(self):
        return self.ChellangeName  # You will get the list with the Challenge name

    class Meta:
        db_table = "Chellange"


class TopicList(models.Model):
    # one too many or many to one relaton
    Chellange = models.ForeignKey(Chellange, on_delete=models.CASCADE)
    Topic = models.CharField(max_length=50, blank=False, null=False)
    TopicDesc = models.TextField(max_length=1000, blank=True, null=True)
    voteCount = models.IntegerField(default=0, null=False, blank=True)
    created_on = models.DateTimeField(auto_now=True )

    def __str__(self):
        return str(self.Topic)+' :  '+self.TopicDesc

    class Meta:
        db_table = "TopicList"

from django.utils import timezone

class Comment(models.Model):
    # id
    Chellange = models.ForeignKey(Chellange, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True, null = False,  blank = False)    
    edit_Session_Expiry = models.DateTimeField(default=hour_hence(1),  null = False,  blank = False, editable = False)
    message = models.TextField('Message Field')

    class Meta:
        db_table = "Comment"


class Vote(models.Model):
    # id
    Chellange = models.ForeignKey(Chellange, on_delete=models.CASCADE)
    Topic = models.ForeignKey(TopicList, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    is_votted = models.BooleanField(default=False)

    class Meta:
        db_table = "Vote"
        unique_together = ('Chellange', 'User',)
        # verbose_name


class testMOdel(models.Model):
    # id
    message = models.TextField('Message Field')

    def __str__(self):
        return self.message

    class Meta:
        db_table = "Test_MOdel"


class Timeline(models.Model):
    #id
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True )  #This one works exact time of current 
    news_header = models.CharField(max_length=500)
    news = models.TextField('Message Field')
    def __str__(self):
        return str(self.user_id)
    class Meta:
        db_table="Timeline"



class contact_us(models.Model):
    email = models.EmailField(max_length=50, blank=False, null=False)
    message = models.TextField(max_length=1000, blank=True, null=False)
    created_on = models.DateTimeField(auto_now=True )
    # date = models.DateTimeField(default=timezone.no)
    # topiclist = models.ForeignKey(TopicList, on_delete=models.CASCADE)
    # def __str__(self):
    #     # You will get the list with the Challenge name
    #     return self.email + '    :   ' + self.message[0:20]+'.......'
    # class Meta:
    #     db_table = "Contact"
    #     verbose_name = 'Contact'
    #     verbose_name_plural = 'Contacts'

    class Meta:
        db_table = "Contact_uss"





from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )