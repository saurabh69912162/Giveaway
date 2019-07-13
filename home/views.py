from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from .models import *
from details.models import *
from django.apps import apps
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import F
from .forms import *
import facebook
import requests
import json


from allauth.socialaccount.models import SocialAccount,SocialToken



def facebook_profile_like_function(fb_id,giveaway_id,sequence_id):
    account = SocialAccount.objects.get(uid=fb_id)
    token = SocialToken.objects.get(account=account)
    model = apps.get_model('details', 'giveaway_rule')
    facebook_page_id_fetch = model.objects.get(giveaway_id = giveaway_id ,sequence_number=sequence_id)
    search  = facebook_page_id_fetch.facebook_profile_like

    graph = facebook.GraphAPI(access_token=token, version="2.12")

    post = graph.get_object(id='me', fields='likes.limit(100)')
    list0 = post['likes']['data']
    new_list0 = []
    for x in range(len(list0)):
        new_list0.append(post['likes']['data'][x]['id'])
    after0 = post['likes']['paging']['next']


    new_list1 = []
    next0 = requests.get(after0)
    answer0 = next0.json()
    list1 = answer0['data']
    for x in range(len(list1)):
        new_list1.append(answer0['data'][x]['id'])
    after1 = answer0['paging']['next']

    new_list2 = []
    next1 = requests.get(after1)
    answer1 = next1.json()
    list2 = answer1['data']
    for x in range(len(list2)):
        new_list2.append(answer1['data'][x]['id'])
    after2 = answer1['paging']['next']

    #
    # print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    # print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    # print(new_list0)
    # print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    # print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    # print(new_list1)
    # print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    # print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    # print(new_list2)


    if search in new_list0:
        obj = model.objects.get(giveaway_id = giveaway_id ,sequence_number=sequence_id)
        obj.completed = True
        obj.status = 'Completed'
        obj.save()
    elif search in new_list1:
        obj = model.objects.get(giveaway_id=giveaway_id, sequence_number=sequence_id)
        obj.completed = True
        obj.status = 'Completed'
        obj.save()
    elif search in new_list2:
        obj = model.objects.get(giveaway_id=giveaway_id, sequence_number=sequence_id)
        obj.completed = True
        obj.status = 'Completed'
        obj.save()
    else:
        print('not found')

def default(request):

    model = "new_giveaway"
    give = apps.get_model('details', model)
    giveaways = give.objects.filter(status="Open")
    if request.user.is_authenticated:
        accounts = SocialAccount.objects.filter(user=request.user).count()

        acc_names = SocialAccount.objects.filter(user=request.user)


        context = {'giveaways':giveaways,
                   'accounts':accounts,
                   'acc_names':acc_names,}
    else:
        context = {'giveaways': giveaways,
                   }

    return render(request,'home/index.html',context)

def profile(request):
    if request.user.is_authenticated:
        name = request.user

        return render(request,'home/profile.html',{'name':name})
    else:
        return redirect('/')


def user(request,user):
    name = user
    model1 = "user_details"
    user_details= apps.get_model('details', model1)
    obj1 = get_object_or_404(user_details, username=name)

    model = "new_giveaway"
    give = apps.get_model('details', model)



    away_id = give.objects.values_list('giveaway_id',flat=True).filter(username=obj1)

    away_details = give.objects.filter(username=obj1)


    model2 = "giveaway_rule"
    give1 = apps.get_model('details', model2)
    rules = give1.objects.filter(username=obj1)


    new_zip = zip(away_details,rules)

    return render(request,'home/user.html',{'name':name,'new_zip':new_zip,'obj1':obj1})


def detailpage(request,user,giveaway_id):
    if request.user.is_authenticated:
        accounts_fb = SocialAccount.objects.filter(user=request.user, provider="facebook")
        accounts_google = SocialAccount.objects.filter(user=request.user, provider="google")
        accounts_twitter = SocialAccount.objects.filter(user=request.user, provider="twitter")


    if request.method == 'POST':
        if "enter" in request.POST:
            model3 = "entry"
            entry = apps.get_model('details', 'entry')
            obj = entry.objects.get_or_create(user=request.user, giveaway_id=giveaway_id)

            entry = apps.get_model('details', 'giveaway_analytics')
            total_participants = entry.objects.filter(giveaway_id=giveaway_id).update(participants_count=F('participants_count') + 1)
            partial_entry = entry.objects.filter(giveaway_id=giveaway_id).update(partial=F('partial') + 1)

        if "insta_profile_follow" in request.POST:
            print('insta follow')

        if "insta_post" in request.POST:
            print('insta_post')

        if "insta_comment" in request.POST:
            print('insta_comment')

        if "facebook_profile_like" in request.POST:
            answer = request.POST['facebook_profile_like']
            fb_id = answer.split(',')[0]
            giveaway_id = answer.split(',')[1]
            sequence_id = answer.split(',')[2]
            acc_fb = SocialAccount.objects.filter(user=request.user, provider="facebook").count()
            new_obj = SocialAccount.objects.filter(user=request.user, provider="facebook",uid=answer)
            facebook_profile_like_function(fb_id,giveaway_id,sequence_id)

        if "facebook_post_like" in request.POST:
            answer = request.POST['facebook_post_like']
            print(answer)
            print('facebook_post_like')


        if "facebook_post_comment" in request.POST:
            answer = request.POST['facebook_post_comment']
            print(answer)
            print('facebook_post_comment')


        if "facebook_post_share" in request.POST:
            answer = request.POST['facebook_post_share']
            print(answer)
            print('facebook_post_share')


        if "twitter_profile_follow" in request.POST:
            answer = request.POST['twitter_profile_follow']
            print(answer)
            print('twitter_profile_follow')

        if "tweet_like" in request.POST:
            answer = request.POST['tweet_like']
            print(answer)
            print('tweet_like')

        if "tweet_comment" in request.POST:
            answer = request.POST['tweet_comment']
            print(answer)
            print('tweet_comment')

        if "retweet" in request.POST:
            answer = request.POST['retweet']
            print(answer)
            print('retweet')

        if "youtube_subscibe" in request.POST:
            answer = request.POST['youtube_subscibe']
            print(answer)
            print('youtube_subscibe')

        if "youtube_comment" in request.POST:
            answer = request.POST['youtube_comment']
            print(answer)
            print('youtube_comment')

        if "youtube_like" in request.POST:
            answer = request.POST['youtube_like']
            print(answer)
            print('youtube_like')

        if "youtube_share" in request.POST:
            answer = request.POST['youtube_share']
            print(answer)
            print('youtube_share')

        if "go_to_this_link" in request.POST:
            print('go_to_this_link')

    model = "new_giveaway"
    give = apps.get_model('details', model)
    giveaways = give.objects.filter(giveaway_id=giveaway_id)

    model2 = "giveaway_rule"
    give1 = apps.get_model('details', model2)
    rules = give1.objects.filter(giveaway_id=giveaway_id)


    entry = apps.get_model('details', 'giveaway_analytics')
    total_ppl = entry.objects.get(giveaway_id=giveaway_id).participants_count



    model3 = "entry"
    give2 = apps.get_model('details', model3)
    check = give2.objects.filter(user = request.user, giveaway_id=giveaway_id)
    if check:
        eligible = "1"
    else:
        eligible = ""

    context = {'user':user,'giveaways':giveaways,
               'rules':rules,'giveaway_id':giveaway_id,
               'eligible':eligible,'total_ppl':total_ppl,
               }

    if request.user.is_authenticated:
        context = {'user': user, 'giveaways': giveaways,
                   'rules': rules, 'giveaway_id': giveaway_id,
                   'eligible': eligible, 'total_ppl': total_ppl,
                   'accounts_fb': accounts_fb,
                   'accounts_google':accounts_google,
                   'accounts_twitter':accounts_twitter}
    return render(request, 'home/details.html', context)


def adminonly(request):
    if request.user.is_authenticated:
        model = apps.get_model('details', 'user_details')
        if model.objects.filter(username=request.user):
            #obj = model.objects.filter(username=request.user)
            model1 = apps.get_model('details', 'new_giveaway')
            obj = model1.objects.filter(username=request.user)

            return render(request, 'home/adminonly.html', {'obj':obj,})

        else:
            return redirect('/')

    else:
        return redirect('/')



def announce_winner(request):
    if request.user.is_authenticated:
        model = apps.get_model('details', 'user_details')
        if model.objects.filter(username=request.user):
            #obj = model.objects.filter(username=request.user)
            model1 = apps.get_model('details', 'new_giveaway')
            obj = model1.objects.filter(username=request.user)

            return render(request, 'home/announcewinner.html', {'obj':obj,})

        else:
            return redirect('/')

    else:
        return redirect('/')


def endpage(request,user,giveaway_id):
    if request.user.is_authenticated:
        model = apps.get_model('details', 'user_details')
        if model.objects.filter(username=request.user):
            #obj = model.objects.filter(username=request.user)
            model1 = apps.get_model('details', 'new_giveaway')
            obj = model1.objects.filter(username=request.user, giveaway_id=giveaway_id)

            model2 = apps.get_model('details', 'giveaway_rule')
            obj1 = model2.objects.filter(giveaway_id=giveaway_id)


            return render(request, 'home/endgiveaway.html', {'obj':obj,'giveaway_id':giveaway_id,'obj1':obj1})

        else:
            return redirect('/')

    else:
        return redirect('/')


def winner(request):
    if request.method == "POST":
        if "facebook" in request.POST:
            name = "facebook"
            uid = request.POST['facebook']
            return render(request, 'home/winner.html', {'name':name,})

        if "youtube" in request.POST:
            name = "yt"
            giveaway_id = request.POST['youtube']

            model2 = apps.get_model('details', 'giveaway_rule')
            obj = model2.objects.filter(giveaway_id=giveaway_id)

            for x in obj:
                if x.sequence_number > 0:
                    if x.youtube_comment:
                        print(x.youtube_comment)

            context = {'obj':obj,'name':name}
            return render(request, 'home/winner.html', context)

        if "twitter" in request.POST:
            name = "twitter"
            uid = request.POST['twitter']

            return render(request, 'home/winner.html', {'name':name,})

        if "rule" in request.POST:
            name = "rule"
            uid = request.POST['rule']
            return render(request, 'home/winner.html', {'name':name,})

        if "random" in request.POST:
            name = "random"
            uid = request.POST['random']
            return render(request, 'home/winner.html', {'name':name,})

        if "lucky" in request.POST:
            name = "lucky"
            uid = request.POST['lucky']
            return render(request, 'home/winner.html', {'name':name,})

        else:
            return redirect('/')
    else:
        return redirect('/')