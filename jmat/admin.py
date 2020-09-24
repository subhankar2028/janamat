from django.contrib import admin
from .models import *
admin.site.site_header = "JANAMAT"


class UserProfileAdmin(admin.ModelAdmin):
    list_display= ('user', 'profile_image', 'phone', 'address', 'country', 'city', 'postal_code')
admin.site.register(UserProfile, UserProfileAdmin)

class ChellangeAdmin(admin.ModelAdmin):
    list_display= ('ChellangeName', 'ChellangeDesc', 'created_on')
admin.site.register(Chellange, ChellangeAdmin)

class TopicListAdmin(admin.ModelAdmin):
    list_display= ('Chellange', 'Topic', 'TopicDesc', 'voteCount', 'created_on',)
admin.site.register(TopicList, TopicListAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display= ('id', 'user', 'Chellange', 'message', 'created_on', 'edit_Session_Expiry', )
admin.site.register(Comment, CommentAdmin)


class VoteAdmin(admin.ModelAdmin):
    list_display= ('Chellange', 'Topic', 'User', 'is_votted')
admin.site.register(Vote, VoteAdmin)


class TimelineAdmin(admin.ModelAdmin):
    list_display= ('user', 'date_time', 'news_header', 'news', )
admin.site.register(Timeline, TimelineAdmin)


class contact_usAdmin(admin.ModelAdmin):
    list_display= ('email', 'message', 'created_on', )
admin.site.register(contact_us, contact_usAdmin)


