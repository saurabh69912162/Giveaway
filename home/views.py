from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from .models import *
from details.models import *
from itertools import count
from django.apps import apps
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import F
from .forms import *
import facebook
import requests
import json
from urllib.parse import urlparse
import requests
import math
import random
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

            context = {'obj':obj,'name':name,'giveaway_id':giveaway_id}
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



def start(vids_list):

    vids = vids_list
    all_comments = []
    global vid_len
    vid_len = len(vids)


    obj = {}
    for i in range(0, vid_len):
        obj[str(i)] = []


    profile_url = {}
    for i in range(0, vid_len):
        profile_url[str(i)] = []


    comment = {}
    for i in range(0, vid_len):
        comment[str(i)] = []

    zip_list = {}
    for i in range(0, vid_len):
        comment[str(i)] = []


    video_count = -1

    for x in vids:
        o = urlparse(x)
        video_id = o.query.split('v=')[1]
        comment_count_request = requests.get('https://www.googleapis.com/youtube/v3/videos?part=id%2C++statistics&id='+video_id+'&key=AIzaSyAON6ej-MZMTh3xHP-uc_sBvZ0s5HXhRvM')
        comment_count_json = comment_count_request.json()
        comment_count = comment_count_json['items'][0]['statistics']['commentCount']

        floorValue = math.ceil(int(comment_count)/100)
        if floorValue == 0:
         set_loop_counter = 1
        else:
         set_loop_counter = floorValue

        print('Comment Count :: ',comment_count)
        print('Loop Count :: ',set_loop_counter)

        for x in range(set_loop_counter):
         if x == 0 and set_loop_counter == 1 :
             video_count = video_count + 1
             page1 = requests.get('https://www.googleapis.com/youtube/v3/commentThreads?part=id%2Csnippet&maxResults=100&videoId='+video_id+'&key=AIzaSyAON6ej-MZMTh3xHP-uc_sBvZ0s5HXhRvM&pageToken=')
             page1_json = page1.json()
             #print(page1_json['items'])
             for y in range(int(comment_count)):
                 try:
                     #print(page1_json['items'][y]['snippet']['topLevelComment']['snippet']['textDisplay'])
                     obj[str(video_count)].append(page1_json['items'][y]['snippet']['topLevelComment']['snippet']['authorDisplayName'])
                     profile_url[str(video_count)].append(page1_json['items'][y]['snippet']['topLevelComment']['snippet']['authorChannelUrl'])
                     comment[str(video_count)].append(page1_json['items'][y]['snippet']['topLevelComment']['snippet']['textDisplay'])


                 except IndexError:
                     break
             break
         else:
             if x == 0:
                 video_count = video_count + 1
                 page1 = requests.get('https://www.googleapis.com/youtube/v3/commentThreads?part=id%2Csnippet&maxResults=100&videoId=' + video_id + '&key=AIzaSyAON6ej-MZMTh3xHP-uc_sBvZ0s5HXhRvM')
                 page1_json = page1.json()
                 next = '&pageToken=' + page1_json['nextPageToken']

                 for y in range(int(comment_count)):
                     try:

                         obj[str(video_count)].append(page1_json['items'][y]['snippet']['topLevelComment']['snippet']['authorDisplayName'])
                         profile_url[str(video_count)].append(page1_json['items'][y]['snippet']['topLevelComment']['snippet']['authorChannelUrl'])
                         comment[str(video_count)].append(page1_json['items'][y]['snippet']['topLevelComment']['snippet']['textDisplay'])
                         #print(page1_json['items'][y]['snippet']['topLevelComment']['snippet']['textDisplay'])


                     except IndexError:
                         break

             elif x>0:

                 page2 = requests.get('https://www.googleapis.com/youtube/v3/commentThreads?part=id%2Csnippet&maxResults=100&videoId='+video_id +'&key=AIzaSyAON6ej-MZMTh3xHP-uc_sBvZ0s5HXhRvM'+next)
                 page2_json = page2.json()
                 try:
                     next = '&pageToken='+page2_json['nextPageToken']
                 except KeyError:
                     pass

                 for y in range(int(comment_count)):
                     try:

                         obj[str(video_count)].append(page1_json['items'][y]['snippet']['topLevelComment']['snippet']['authorDisplayName'])
                         profile_url[str(video_count)].append(page1_json['items'][y]['snippet']['topLevelComment']['snippet']['authorChannelUrl'])
                         comment[str(video_count)].append(page1_json['items'][y]['snippet']['topLevelComment']['snippet']['textDisplay'])

                     except IndexError:
                         break


             else:
                 pass


        #print('Finale')
        #print(all_comments)
        print('$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%')
        print('$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%')



        def set_me(count):
            if count == 1:
                pass

            if count == 2:
                name_user = []
                url_user = []
                comment_user = []
                answer = set(obj['0']).intersection(obj['1'])
                print(answer)
                print(len(answer))
                for xyz in answer:
                    for i in range(0, 2):
                        doit = zip(obj[str(i)], profile_url[str(i)], comment[str(i)])
                        for x, y, z in doit:
                            if xyz in x:
                                name_user.append(x)
                                url_user.append(y)
                                comment_user.append(z)
                                break
                return name_user, url_user, comment_user

            if count == 3:
                name_user = []
                url_user = []
                comment_user = []

                answer = set(obj['0']).intersection(obj['1'], obj['2'])
                print(answer)
                print(len(answer))
                for xyz in answer:
                    for i in range(0, 3):
                        doit = zip(obj[str(i)], profile_url[str(i)], comment[str(i)])
                        for x, y, z in doit:
                            if xyz in x:
                                name_user.append(x)
                                url_user.append(y)
                                comment_user.append(z)
                                break
                return name_user,url_user,comment_user



            if count == 4:

                answer = set(obj['0']).intersection(obj['0'], obj['1'], obj['2'], obj['3'])
                print(answer)
                print(len(answer))
                for xyz in answer:
                    for i in range(0, 4):
                        doit = zip(obj[str(i)], profile_url[str(i)], comment[str(i)])
                        for x, y, z in doit:
                            if xyz in x:
                                print(x)
                                print(y)
                                print(z)
                                break

            if count == 5:

                answer = set(obj['0']).intersection(obj['0'], obj['1'], obj['2'], obj['3'], obj['4'])
                print(answer)
                print(len(answer))
                for xyz in answer:
                    for i in range(0, 5):
                        doit = zip(obj[str(i)], profile_url[str(i)], comment[str(i)])
                        for x, y, z in doit:
                            if xyz in x:
                                print(x)
                                print(y)
                                print(z)
                                break

            if count == 6:

                answer = set(obj['0']).intersection(obj['0'], obj['1'], obj['2'], obj['3'], obj['4'], obj['5'])
                print(answer)
                print(len(answer))
                for xyz in answer:
                    for i in range(0, 6):
                        doit = zip(obj[str(i)], profile_url[str(i)], comment[str(i)])
                        for x, y, z in doit:
                            if xyz in x:
                                print(x)
                                print(y)
                                print(z)
                                break

            if count == 7:

                answer = set(obj['0']).intersection(obj['0'], obj['1'], obj['2'], obj['3'], obj['4'], obj['5'],
                                                    obj['6'])
                print(answer)
                print(len(answer))
                for xyz in answer:
                    for i in range(0, 7):
                        doit = zip(obj[str(i)], profile_url[str(i)], comment[str(i)])
                        for x, y, z in doit:
                            if xyz in x:
                                print(x)
                                print(y)
                                print(z)
                                break

            if count == 8:

                answer = []
                answer = set(obj['0']).intersection(obj['0'], obj['1'], obj['2'], obj['3'], obj['4'], obj['5'],
                                                    obj['6'], obj['7'])
                print(answer)
                print(len(answer))
                for xyz in answer:
                    for i in range(0, 8):
                        doit = zip(obj[str(i)], profile_url[str(i)], comment[str(i)])
                        for x, y, z in doit:
                            if xyz in x:
                                print(x)
                                print(y)
                                print(z)
                                break

            if count == 9:
                answer = []
                answer = set(obj['0']).intersection(obj['0'], obj['1'], obj['2'], obj['3'], obj['4'], obj['5'],
                                                    obj['6'],
                                                    obj['7'], obj['8'])

                print(answer)
                print(len(answer))
                for xyz in answer:
                    for i in range(0, 9):
                        doit = zip(obj[str(i)], profile_url[str(i)], comment[str(i)])
                        for x, y, z in doit:
                            if xyz in x:
                                print(x)
                                print(y)
                                print(z)
                                break

            if count == 10:
                answer = []
                answer = set(obj['0']).intersection(obj['0'], obj['1'], obj['2'], obj['3'], obj['4'], obj['5'],
                                                    obj['6'],
                                                    obj['7'], obj['8'], obj['9'])
                print(answer)
                print(len(answer))
                for xyz in answer:
                    for i in range(0, 10):
                        doit = zip(obj[str(i)], profile_url[str(i)], comment[str(i)])
                        for x, y, z in doit:
                            if xyz in x:
                                print(x)
                                print(y)
                                print(z)
                                break

            if count == 11:
                answer = []
                answer = set(obj['0']).intersection(obj['0'], obj['1'], obj['2'], obj['3'], obj['4'], obj['5'],
                                                    obj['6'],
                                                    obj['7'], obj['8'], obj['9'], obj['10'])

                print(answer)
                print(len(answer))
                for xyz in answer:
                    for i in range(0, 11):
                        doit = zip(obj[str(i)], profile_url[str(i)], comment[str(i)])
                        for x, y, z in doit:
                            if xyz in x:
                                print(x)
                                print(y)
                                print(z)
                                break

            if count == 12:
                answer = []
                answer = set(obj['0']).intersection(obj['0'], obj['1'], obj['2'], obj['3'], obj['4'], obj['5'],
                                                    obj['6'], obj['7'], obj['8'], obj['9'], obj['10'], obj['11'])
                print(answer)
                print(len(answer))
                for xyz in answer:
                    for i in range(0, 12):
                        doit = zip(obj[str(i)], profile_url[str(i)], comment[str(i)])
                        for x, y, z in doit:
                            if xyz in x:
                                print(x)
                                print(y)
                                print(z)
                                break

            if count == 13:
                answer = []
                answer = set(obj['0']).intersection(obj['0'], obj['1'], obj['2'], obj['3'], obj['4'], obj['5'],
                                                    obj['6'], obj['7'], obj['8'], obj['9'], obj['10'], obj['11'],
                                                    obj['12'])
                print(answer)
                print(len(answer))
                for xyz in answer:
                    for i in range(0, 13):
                        doit = zip(obj[str(i)], profile_url[str(i)], comment[str(i)])
                        for x, y, z in doit:
                            if xyz in x:
                                print(x)
                                print(y)
                                print(z)
                                break

            if count == 14:
                answer = []
                answer = set(obj['0']).intersection(obj['0'], obj['1'], obj['2'], obj['3'], obj['4'], obj['5'],
                                                    obj['6'], obj['7'], obj['8'], obj['9'], obj['10'], obj['11'],
                                                    obj['12'], obj['13'])
                print(answer)
                print(len(answer))
                for xyz in answer:
                    for i in range(0, 14):
                        doit = zip(obj[str(i)], profile_url[str(i)], comment[str(i)])
                        for x, y, z in doit:
                            if xyz in x:
                                print(x)
                                print(y)
                                print(z)
                                break

            if count == 15:

                answer = []
                answer = set(obj['0']).intersection(obj['0'], obj['1'], obj['2'], obj['3'], obj['4'], obj['5'],
                                                    obj['6'], obj['7'], obj['8'], obj['9'], obj['10'], obj['11'],
                                                    obj['12'], obj['13'], obj['14'])
                print(answer)
                print(len(answer))
                for xyz in answer:
                    for i in range(0, 15):
                        doit = zip(obj[str(i)], profile_url[str(i)], comment[str(i)])
                        for x, y, z in doit:
                            if xyz in x:
                                print(x)
                                print(y)
                                print(z)
                                break

            if count == 16:

                answer = []
                answer = set(obj['0']).intersection(obj['0'], obj['1'], obj['2'], obj['3'], obj['4'], obj['5'],
                                                    obj['6'], obj['7'], obj['8'], obj['9'], obj['10'], obj['11'],
                                                    obj['12'], obj['13'], obj['14'], obj['15'])
                print(answer)
                print(len(answer))
                for xyz in answer:
                    for i in range(0, 16):
                        doit = zip(obj[str(i)], profile_url[str(i)], comment[str(i)])
                        for x, y, z in doit:
                            if xyz in x:
                                print(x)
                                print(y)
                                print(z)
                                break

    return set_me(vid_len)



def ytcomments(request,giveaway_id):

    model2 = apps.get_model('details', 'giveaway_rule')
    obj = model2.objects.filter(giveaway_id=giveaway_id)
    vids_list = []
    for x in obj:
        if x.sequence_number > 0:
            if x.youtube_comment:
                vids_list.append(x.youtube_comment)

    name_user,url_user,comment_user = start(vids_list)


    win_zip = zip(name_user,url_user,comment_user)


    win_zip1 = list(zip(name_user, url_user, comment_user))

    random.shuffle(win_zip1)

    a,b,c = zip(*win_zip1)
    random_list = zip(count(),a,b,c)

    # print(random.sample(range(0, len(name_user)), len(name_user)))

    context = {'vids_list':vids_list,
              'win_zip':win_zip,
               'random_list':random_list,
                }
    return render(request, 'home/ytcomments.html',context)

from django.db.models import Max

def add_modify_rules(request,user,giveaway_id):

    model1 = apps.get_model('details', 'new_giveaway')
    obj1 = model1.objects.get(giveaway_id=giveaway_id)

    model = apps.get_model('details', 'giveaway_rule')
    obj = model.objects.filter(giveaway_id = giveaway_id)
    max_rating = model.objects.filter(giveaway_id = giveaway_id).aggregate(Max('sequence_number'))




    user_obj = user_details.objects.get(username = user)

    form = rules_form()
    if request.method == 'POST':
        if 'Rule' in request.POST:
            if 'insta_profile_follow' in request.POST['Rule']:
                obj12 = model()
                obj12.giveaway_name = obj1.giveaway_title
                obj12.username = user_obj
                obj12.sequence_number = 99
                obj12.giveaway_id = giveaway_id
                obj12.insta_profile_follow = request.POST['link']
                obj12.save()

            if 'insta_post' in request.POST['Rule']:
                obj12 = model()
                obj12.giveaway_name = obj1.giveaway_title
                obj12.username = user_obj
                obj12.sequence_number = 99
                obj12.giveaway_id = giveaway_id
                obj12.insta_post = request.POST['link']
                obj12.save()
            if 'insta_comment' in request.POST['Rule']:
                obj12 = model()
                obj12.giveaway_name = obj1.giveaway_title
                obj12.username = user_obj
                obj12.sequence_number = 99
                obj12.giveaway_id = giveaway_id
                obj12.insta_comment = request.POST['link']
                obj12.save()
            if 'facebook_profile_like' in request.POST['Rule']:
                obj12 = model()
                obj12.giveaway_name = obj1.giveaway_title
                obj12.username = user_obj
                obj12.sequence_number = 99
                obj12.giveaway_id = giveaway_id
                obj12.facebook_profile_like = request.POST['link']
                obj12.save()
            if 'facebook_post_like' in request.POST['Rule']:
                obj12 = model()
                obj12.giveaway_name = obj1.giveaway_title
                obj12.username = user_obj
                obj12.sequence_number = 99
                obj12.giveaway_id = giveaway_id
                obj12.facebook_post_like = request.POST['link']
                obj12.save()
            if 'facebook_post_comment' in request.POST['Rule']:
                obj12 = model()
                obj12.giveaway_name = obj1.giveaway_title
                obj12.username = user_obj
                obj12.sequence_number = 99
                obj12.giveaway_id = giveaway_id
                obj12.facebook_post_comment = request.POST['link']
                obj12.save()
            if 'facebook_post_share' in request.POST['Rule']:
                obj12 = model()
                obj12.giveaway_name = obj1.giveaway_title
                obj12.username = user_obj
                obj12.sequence_number = 99
                obj12.giveaway_id = giveaway_id
                obj12.facebook_post_share = request.POST['link']
                obj12.save()
            if 'twitter_profile_follow' in request.POST['Rule']:
                obj12 = model()
                obj12.giveaway_name = obj1.giveaway_title
                obj12.username = user_obj
                obj12.sequence_number = 99
                obj12.giveaway_id = giveaway_id
                obj12.twitter_profile_follow = request.POST['link']
                obj12.save()
            if 'tweet_like' in request.POST['Rule']:
                obj12 = model()
                obj12.giveaway_name = obj1.giveaway_title
                obj12.username = user_obj
                obj12.sequence_number = 99
                obj12.giveaway_id = giveaway_id
                obj12.tweet_like = request.POST['link']
                obj12.save()
            if 'tweet_comment' in request.POST['Rule']:
                obj12 = model()
                obj12.giveaway_name = obj1.giveaway_title
                obj12.username = user_obj
                obj12.sequence_number = 99
                obj12.giveaway_id = giveaway_id
                obj12.tweet_comment = request.POST['link']
                obj12.save()
            if 'retweet' in request.POST['Rule']:
                obj12 = model()
                obj12.giveaway_name = obj1.giveaway_title
                obj12.username = user_obj
                obj12.sequence_number = 99
                obj12.giveaway_id = giveaway_id
                obj12.retweet = request.POST['link']
                obj12.save()
            if 'youtube_subscibe' in request.POST['Rule']:
                obj12 = model()
                obj12.giveaway_name = obj1.giveaway_title
                obj12.username = user_obj
                obj12.sequence_number = 99
                obj12.giveaway_id = giveaway_id
                obj12.youtube_subscibe = request.POST['link']
                obj12.save()
            if 'youtube_comment' in request.POST['Rule']:
                obj12 = model()
                obj12.giveaway_name = obj1.giveaway_title
                obj12.username = user_obj
                obj12.sequence_number = 99
                obj12.giveaway_id = giveaway_id
                obj12.youtube_comment = request.POST['link']
                obj12.save()
            if 'youtube_like' in request.POST['Rule']:
                obj12 = model()
                obj12.giveaway_name = obj1.giveaway_title
                obj12.username = user_obj
                obj12.sequence_number = 99
                obj12.giveaway_id = giveaway_id
                obj12.youtube_like = request.POST['link']
                obj12.save()
            if 'go_to_this_link' in request.POST['Rule']:
                obj12 = model()
                obj12.giveaway_name = obj1.giveaway_title
                obj12.username = user_obj
                obj12.sequence_number = 99
                obj12.giveaway_id = giveaway_id
                obj12.go_to_this_link = request.POST['link']
                obj12.save()
            if 'youtube_share' in request.POST['Rule']:
                obj12 = model()
                obj12.giveaway_name = obj1.giveaway_title
                obj12.username = user_obj
                obj12.sequence_number = 99
                obj12.giveaway_id = giveaway_id
                obj12.youtube_share = request.POST['link']
                obj12.save()
    return render(request,'home/add_modify_rules.html',{'form':form,'obj':obj})

from django.db.models import Count
import time
def comment_frequency(request,giveaway_id):
    model = apps.get_model('details', 'comments')
    model2 = apps.get_model('details', 'giveaway_rule')
    obj = model2.objects.filter(giveaway_id=giveaway_id)
    vids_list = []
    for x in obj:
        if x.sequence_number > 0:
            if x.youtube_comment:
                vids_list.append(x.youtube_comment)

    vids = vids_list
    all_comments = []
    global vid_len
    vid_len = len(vids)

    frequency_comment = []
    frequency_name = []
    frequency_url = []
    frequency = []

    for video_count in vids:
        o = urlparse(video_count)
        video_id = o.query.split('v=')[1]

        comment_count_request = requests.get(
            'https://www.googleapis.com/youtube/v3/videos?part=id%2C++statistics&id=' + video_id + '&key=AIzaSyAON6ej-MZMTh3xHP-uc_sBvZ0s5HXhRvM')
        comment_count_json = comment_count_request.json()
        comment_count = comment_count_json['items'][0]['statistics']['commentCount']
        floorValue = math.ceil(int(comment_count) / 100)
        if floorValue == 0:
            set_loop_counter = 1
        else:
            set_loop_counter = floorValue

        print('Comment Count :: ', comment_count)
        print('Loop Count :: ', set_loop_counter)

        for single_video in range(set_loop_counter):
            if single_video == 0 and set_loop_counter == 1:
                print(video_count)
                page1 = requests.get(
                    'https://www.googleapis.com/youtube/v3/commentThreads?part=id%2Csnippet&maxResults=100&videoId=' + video_id + '&key=AIzaSyAON6ej-MZMTh3xHP-uc_sBvZ0s5HXhRvM')
                page1_json = page1.json()
                for y in range(int(comment_count)):
                    try:
                        # print(page1_json['items'][y]['snippet']['topLevelComment']['snippet']['textDisplay'])
                        # frequency_url.append(
                        #     page1_json['items'][y]['snippet']['topLevelComment']['snippet']['textDisplay'])
                        check_exist = model.objects.filter(url = page1_json['items'][y]['snippet']['topLevelComment']['snippet']['authorChannelUrl'])
                        if check_exist:
                            model.objects.filter(url = page1_json['items'][y]['snippet']['topLevelComment']['snippet']['authorChannelUrl']).update(count=F('count') + 1)
                            obj = model.objects.get(url=page1_json['items'][y]['snippet']['topLevelComment']['snippet']['authorChannelUrl'])
                            obj.comment  +=':: COMMENT ::' +  page1_json['items'][y]['snippet']['topLevelComment']['snippet'][
                                'textDisplay']
                            obj.save()
                        else:
                            obj_comment = model()
                            obj_comment.comment = page1_json['items'][y]['snippet']['topLevelComment']['snippet'][
                                'textDisplay']
                            obj_comment.name = page1_json['items'][y]['snippet']['topLevelComment']['snippet'][
                                'authorDisplayName']
                            obj_comment.url = page1_json['items'][y]['snippet']['topLevelComment']['snippet'][
                                'authorChannelUrl']
                            obj_comment.save()
                        print(page1_json['items'][y]['snippet']['topLevelComment']['snippet']['textDisplay'])
                    except IndexError:
                        break

            elif single_video == 0 and set_loop_counter > 1:
                print('0 and 1', video_count)
                page1 = requests.get(
                    'https://www.googleapis.com/youtube/v3/commentThreads?part=id%2Csnippet&maxResults=100&videoId=' + video_id + '&key=AIzaSyAON6ej-MZMTh3xHP-uc_sBvZ0s5HXhRvM')
                page1_json = page1.json()
                try:
                    next = '&pageToken=' + page1_json['nextPageToken']
                except KeyError:
                    pass
                #next = '&pageToken=' + page1_json['nextPageToken']

                for y in range(int(comment_count)):
                    try:
                        check_exist = model.objects.filter(
                            url=page1_json['items'][y]['snippet']['topLevelComment']['snippet']['authorChannelUrl'])
                        if check_exist:
                            model.objects.filter(url=page1_json['items'][y]['snippet']['topLevelComment']['snippet'][
                                'authorChannelUrl']).update(count=F('count') + 1)
                            obj = model.objects.get(
                                url=page1_json['items'][y]['snippet']['topLevelComment']['snippet']['authorChannelUrl'])
                            obj.comment += ':: COMMENT ::' + page1_json['items'][y]['snippet']['topLevelComment']['snippet'][
                                'textDisplay']
                            obj.save()
                        else:
                            obj_comment = model()
                            obj_comment.comment = page1_json['items'][y]['snippet']['topLevelComment']['snippet'][
                                'textDisplay']
                            obj_comment.name = page1_json['items'][y]['snippet']['topLevelComment']['snippet'][
                                'authorDisplayName']
                            obj_comment.url = page1_json['items'][y]['snippet']['topLevelComment']['snippet'][
                                'authorChannelUrl']
                            obj_comment.save()
                        #     page1_json['items'][y]['snippet']['topLevelComment']['snippet']['textDisplay'])
                        print(page1_json['items'][y]['snippet']['topLevelComment']['snippet']['textDisplay'])
                    except IndexError:
                        break

            elif set_loop_counter > 1:

                print('> 1', video_count)
                page1 = requests.get(
                    'https://www.googleapis.com/youtube/v3/commentThreads?part=id%2Csnippet&maxResults=100&videoId=' + video_id + '&key=AIzaSyAON6ej-MZMTh3xHP-uc_sBvZ0s5HXhRvM' + next)
                page1_json = page1.json()
                print(next)
                try:
                    next = '&pageToken=' + page1_json['nextPageToken']
                except KeyError:
                    pass
                # next = '&pageToken=' + page1_json['nextPageToken']
                for y in range(int(comment_count)):
                    try:
                        check_exist = model.objects.filter(
                            url=page1_json['items'][y]['snippet']['topLevelComment']['snippet']['authorChannelUrl'])
                        if check_exist:
                            model.objects.filter(url=page1_json['items'][y]['snippet']['topLevelComment']['snippet'][
                                'authorChannelUrl']).update(count=F('count') + 1)
                            obj = model.objects.get(
                                url=page1_json['items'][y]['snippet']['topLevelComment']['snippet']['authorChannelUrl'])
                            obj.comment += ':: COMMENT ::' + page1_json['items'][y]['snippet']['topLevelComment']['snippet'][
                                'textDisplay']
                            obj.save()
                        else:
                            obj_comment = model()
                            obj_comment.comment = page1_json['items'][y]['snippet']['topLevelComment']['snippet'][
                                'textDisplay']
                            obj_comment.name = page1_json['items'][y]['snippet']['topLevelComment']['snippet'][
                                'authorDisplayName']
                            obj_comment.url = page1_json['items'][y]['snippet']['topLevelComment']['snippet'][
                                'authorChannelUrl']
                            obj_comment.save()
                        print(page1_json['items'][y]['snippet']['topLevelComment']['snippet']['textDisplay'])
                    except IndexError:
                        break
                print(next)
            else:
                print('hi', video_count)



    #ok = sorted(set(model.objects.all().values_list('url').annotate(freq=Count("url"))), reverse=False)
    okay = model.objects.exclude(name = 'Creative Pavan').order_by('-count',)
    #ok = set(model.objects.all().annotate(frequency = Count('url')))
    return render(request,'home/frequency.html',{'okay':okay,})



def cleanmydb(request):
    model = apps.get_model('details', 'comments')
    model.objects.all().delete()
    return redirect('/')



def addgiveaway(request):
    form = add_new_giveaway()
    if request.method == 'POST':
        form = add_new_giveaway(request.POST,request.FILES)
        if form.is_valid():
            form.username = request.user
            form.status = 'Open'
            form.save()
    return render(request, 'home/addnew.html', {'form':form,})
