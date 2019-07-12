# from django.test import TestCase
# from urllib.parse import urlparse
#
# o = urlparse('https://www.facebook.com/permalink.php?story_fbid=2321006788227886&id=1740315322963705')
#
# answer = o.query
# final = answer.split('=')
#
# print(final[2].split('&__')[0]+'_'+final[1].split('&id')[0])




# from django.test import TestCase
from urllib.parse import urlparse
import requests
import math
from collections import Counter


#
# o = urlparse('https://www.facebook.com/permalink.php?story_fbid=2321006788227886&id=1740315322963705')
#
# answer = o.query
# final = answer.split('=')
#
# print(final[2].split('&__')[0]+'_'+final[1].split('&id')[0])



url = 'https://www.youtube.com/watch?v=KoZM4M9U7GM'
url1 = 'https://www.youtube.com/watch?v=giSFVAjrpmA'
url2 = 'https://www.youtube.com/watch?v=7nMYcZ-0V1o'

vids = [url,url1]
all_comments = []

obj = {}
for i in range(0, len(vids)):
    obj[str(i)] = []


profile_url = {}
for i in range(0, len(vids)):
    profile_url[str(i)] = []


comment = {}
for i in range(0, len(vids)):
    comment[str(i)] = []


zip_list = {}
for i in range(0, len(vids)):
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
             print('value is',set_loop_counter,x)
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

#a = dict(Counter(all_comments))
# list1 = zip(a.values(),a.items())
# print(sorted(a.values(),a.items()))
# for x,y in list1:
#  print(x,y)



# print(obj['0'])
# print(obj['1'])
# print(obj['2'])

doit = zip(obj['0'],profile_url['0'],comment['0'])

doit1 = zip(obj['1'],profile_url['1'],comment['1'])



# for x,y,z in doit1:
#     print(x,y,z)
#
# print('$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%')
# print('$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%')
# for x in range(1):
#     print(set(obj[str(x)]).intersection(obj[str(x+1)]))
# print('$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%')
# print('$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%')
# print(set(obj['0']).intersection(obj['1'],obj['2']))
#
























# o = urlparse(url)
# video_id = o.query.split('v=')[1]
# comment_count_request = requests.get('https://www.googleapis.com/youtube/v3/videos?part=id%2C++statistics&id='+video_id+'&key=AIzaSyAON6ej-MZMTh3xHP-uc_sBvZ0s5HXhRvM')
# comment_count_json = comment_count_request.json()
# comment_count = comment_count_json['items'][0]['statistics']['commentCount']
#
# floorValue = math.floor(int(comment_count)/100)
# if floorValue == 0:
#     set_loop_counter = 1
# else:
#     set_loop_counter = floorValue
#
# print('Comment Count :: ',comment_count)
# print('Loop Count :: ',set_loop_counter)
# all_comments = []
#
# for x in range(set_loop_counter):
#     if x == 0 and set_loop_counter == 1 :
#         page1 = requests.get('https://www.googleapis.com/youtube/v3/commentThreads?part=id%2Csnippet&maxResults=100&videoId='+video_id+'&key=AIzaSyAON6ej-MZMTh3xHP-uc_sBvZ0s5HXhRvM&pageToken=')
#         page1_json = page1.json()
#         print(page1_json['items'])
#         for x in range(int(comment_count)):
#             try:
#                 print(page1_json['items'][x]['snippet']['topLevelComment']['snippet']['authorChannelUrl'],'-->',page1_json['items'][x]['snippet']['topLevelComment']['snippet']['authorDisplayName'])
#                 all_comments.append(page1_json['items'][x]['snippet']['topLevelComment']['snippet']['textDisplay'])
#             except IndexError:
#                 break
#         break
#     else:
#         if x == 0:
#             page1 = requests.get('https://www.googleapis.com/youtube/v3/commentThreads?part=id%2Csnippet&maxResults=100&videoId=' + video_id + '&key=AIzaSyAON6ej-MZMTh3xHP-uc_sBvZ0s5HXhRvM')
#             page1_json = page1.json()
#             next = '&pageToken=' + page1_json['nextPageToken']
#
#             for x in range(int(comment_count)):
#                 try:
#                     #print(page1_json['items'][x]['snippet']['topLevelComment']['snippet']['textDisplay'])
#                     all_comments.append(page1_json['items'][x]['snippet']['topLevelComment']['snippet']['textDisplay'])
#                     print(page2_json['items'][x]['snippet']['topLevelComment']['snippet']['textDisplay'])
#                 except IndexError:
#                     break
#
#         elif x>0:
#             page2 = requests.get('https://www.googleapis.com/youtube/v3/commentThreads?part=id%2Csnippet&maxResults=100&videoId='+video_id +'&key=AIzaSyAON6ej-MZMTh3xHP-uc_sBvZ0s5HXhRvM'+next)
#             page2_json = page2.json()
#             next = '&pageToken='+page2_json['nextPageToken']
#
#             for x in range(int(comment_count)):
#                 try:
#                     print(page2_json['items'][x]['snippet']['topLevelComment']['snippet']['textDisplay'])
#                     all_comments.append(page2_json['items'][x]['snippet']['topLevelComment']['snippet']['textDisplay'])
#                 except IndexError:
#                     break
#         else:
#             pass
#
# print('$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%')
# print('$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%')
# print('$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%')
# print('$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%$%')
# print(all_comments)

# page1 = requests.get('https://www.googleapis.com/youtube/v3/commentThreads?part=id%2Csnippet&maxResults=100&videoId='+video_id+'&key=AIzaSyAON6ej-MZMTh3xHP-uc_sBvZ0s5HXhRvM')
# page1_json = page1.json()
# print(page1_json)
#
#
# page2 = requests.get('https://www.googleapis.com/youtube/v3/commentThreads?part=id%2Csnippet&maxResults=100&videoId='+video_id+'&key=AIzaSyAON6ej-MZMTh3xHP-uc_sBvZ0s5HXhRvM&pageToken='+page1_json['nextPageToken'])
# page2_json = page2.json()
# print(page2_json['pageInfo'])
#
# page3 = requests.get('https://www.googleapis.com/youtube/v3/commentThreads?part=id%2Csnippet&maxResults=100&videoId='+video_id+'&key=AIzaSyAON6ej-MZMTh3xHP-uc_sBvZ0s5HXhRvM&pageToken='+page2_json['nextPageToken'])
# page3_json = page2.json()
# print(page3_json['pageInfo'])
#
#
# page4 = requests.get('https://www.googleapis.com/youtube/v3/commentThreads?part=id%2Csnippet&maxResults=100&videoId='+video_id+'&key=AIzaSyAON6ej-MZMTh3xHP-uc_sBvZ0s5HXhRvM&pageToken='+page3_json['nextPageToken'])
# page4_json = page3.json()
# print(page4_json['pageInfo'])
#
# page5 = requests.get('https://www.googleapis.com/youtube/v3/commentThreads?part=id%2Csnippet&maxResults=100&videoId='+video_id+'&key=AIzaSyAON6ej-MZMTh3xHP-uc_sBvZ0s5HXhRvM&pageToken='+page4_json['nextPageToken'])
# page5_json = page5.json()
# print(page5_json['pageInfo'])
#
# page6 = requests.get('https://www.googleapis.com/youtube/v3/commentThreads?part=id%2Csnippet&maxResults=100&videoId='+video_id+'&key=AIzaSyAON6ej-MZMTh3xHP-uc_sBvZ0s5HXhRvM&pageToken='+page5_json['nextPageToken'])
# page6_json = page6.json()
# print(page6_json['pageInfo'])
#



# for x in range(int(comment_count)):
#     try:
#         print(page1_json['items'][x]['snippet']['topLevelComment']['snippet']['authorDisplayName'])
#         print(page1_json['items'][x]['snippet']['topLevelComment']['snippet']['textDisplay'])
#     except IndexError:
#         break
