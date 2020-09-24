from django.shortcuts import render
from django.http import HttpResponse
from . models import *
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from django.db.models import F


def user_credential(request):
    if request.session.has_key('is_logged'):
        user = User.objects.get(username=request.session['username'])
        userProfile = UserProfile.objects.get(
            user=User.objects.get(username=user))
        firstName = user.first_name
        lastName = user.last_name
        profileImage = userProfile.profile_image
        if profileImage == "":
            profileImage = False
        user_context = {
            'user':   user,
            'userProfile':   userProfile,
            'firstName':   firstName,
            'lastName':   lastName,
            'profileImage':   profileImage
        }
        return user_context
    return {}




def Chellange_list_context(request):
    timeline = timelineOBJ(request)
    Chellange_list = Chellange.objects.all()
    context = {
        'timeline': timeline,
        'Chellange_list':   Chellange_list,
    }
    return context



# def timelineOBJ(request):
#     timeline_obj = range(1, 1000)
#     page = request.GET.get('page', 1)
#     paginator = Paginator(timeline_obj, 10)
#     try:
#         timeline = paginator.page(page)
#     except PageNotAnInteger:
#         timeline = paginator.page(1)
#     except EmptyPage:
#         timeline = paginator.page(paginator.num_pages)
#     return timeline


def timelineOBJ(request):
    timeline_obj = Timeline.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(timeline_obj, 10)
    try:
        timeline = paginator.page(page)
    except PageNotAnInteger:
        timeline = paginator.page(1)
    except EmptyPage:
        timeline = paginator.page(paginator.num_pages)
    return timeline


def home(request):
    if request.method == 'GET':  # http://127.0.0.1:8000/
        context = Chellange_list_context(request)
        if request.GET:  # http://127.0.0.1:8000/?Chellange_id=1
            try:
                Chellange_id = request.GET['Chellange_id']
            except:
                timeline = timelineOBJ(request)
                return render(request, 'timeline.html', context={'timeline' : timeline})
                
            selected_Chellange = Chellange.objects.get(id=Chellange_id)
            topic_list = TopicList.objects.filter(Chellange_id=Chellange_id)
            votes = Vote.objects.filter(Chellange_id=Chellange_id)
            comment_list = Comment.objects.filter(Chellange_id=Chellange_id)
            try:
                user = User.objects.get(username=request.session['username'])
                is_votted = Vote.objects.get(
                    User_id=user.id, Chellange_id=Chellange_id).is_votted
            except:
                is_votted = False
            context = {
                'Chellange_list':   Chellange.objects.all(),
                'selected_Chellange':   selected_Chellange,
                'topic_list':   topic_list,
                'comment_list':   comment_list,
                'is_logged':   request.session.has_key('is_logged'),
                'is_votted':   is_votted,
            }
            context.update(user_credential(request))
            return render(request, 'vote.html', context=context)
        context.update(user_credential(request))
        return render(request, 'timeline.html', context=context)
    # Execute this block when user is have just login
    context = Chellange_list_context(request)
    context.update(user_credential(request))
    return render(request, 'timeline.html', context=context)


# def signup(request):
#     pass


def signup(request):
    if request.method == 'GET':
        return render(request, 'signin.html', context={})
    else:
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        UserName = request.POST['username']
        UserName_qs = User.objects.filter(username=UserName)
        if UserName_qs.exists():
            messages.error(request, 'user already exiest')
            return render(request, 'signin.html', context={})
        else:

            if password == cpassword:
                # UserName = email.split('@')[0]
                u = User(username=UserName, first_name=firstname,
                         last_name=lastname, email=email)  # Django user model
                u.save()
                u.set_password(cpassword)
                u.save()
                up = UserProfile(user=u, dob=datetime.now(), phone=phone, )
                up.save()
                return render(request, 'signin.html', context={})
            else:
                messages.error(request, 'password does not match')
                return render(request, 'signin.html', context={})

from rest_framework.authtoken.models import Token

def signin(request):
    if request.method == 'GET':
        if request.session.has_key('is_logged'):
            return home(request)
        else:
            return render(request, 'signin.html', context={})
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        # token = Token.objects.create(user=User.objects.filter(username = user))
        # print(token.key)

        if not user:
            messages.error(request, 'Please check your username and password')
            return render(request, 'signIn.html', context={})
            # context = {"is_SigninFailed": "Sign in failed."}
        # if not user.check_password(password):
        #     messages.error(request, 'Please check password')
        #     return render(request, 'signIn.html', context={})
        else:
            user.last_login = datetime.today()
            user.save()
            request.session['is_logged'] = True
            request.session['username'] = username
            login(request, user)
            return home(request)
        # else:
        #     if not user:
        #         messages.error(request, 'Username does not exiest')
        #         return render(request, 'signIn.html', context={})
        #     # context = {"is_SigninFailed": "Sign in failed."}
        #     if not user.check_password(password):
        #         messages.error(request, 'Please check password')
        #         return render(request, 'signIn.html', context={})


def signout(request):
    logout(request)
    return home(request)


def acceptVote(request):
    if request.method == 'GET':
        topic = TopicList.objects.get(id=request.GET['topic_id'])
        user = User.objects.get(username=request.session['username'])
        try:
            vote = Vote.objects.get(
                User_id=user.id, Chellange_id=topic.Chellange_id)
            return HttpResponse('Votting already done ')
        except:
            vote = Vote(Chellange_id=topic.Chellange_id,
                        Topic_id=request.GET['topic_id'], User_id=user.id, is_votted=True)
            vote.save()
            TopicList.objects.filter(id=request.GET['topic_id']).update(voteCount=F("voteCount") + 1)
            TopicList.objects.filter(id=request.GET['topic_id']).update(voteCount=F("voteCount") + 1)

            # return HttpResponse('Votting Done Successfully in : ' + str(vote.Topic))
            return HttpResponse('Votting Done Successfully.')



def test(request):
    comments = Comment.objects.all()
    return render(request, 'test.html', context={'posts': comments})
    # return render(request, 'ajaxTest.html', context={'posts': comments})




from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def samplehome(request):
    timeline_obj = range(1, 1000)
    page = request.GET.get('page', 1)
    paginator = Paginator(timeline_obj, 20)
    try:
        timeline = paginator.page(page)
    except PageNotAnInteger:
        timeline = paginator.page(1)
    except EmptyPage:
        timeline = paginator.page(paginator.num_pages)

    return render(request, 'sampleHome.html', {'timeline': timeline})
    # return render(request, 'sampleBase.html', {'timeline': timeline})