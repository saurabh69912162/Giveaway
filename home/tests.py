#https://www.googleapis.com/youtube/v3/search?key=AIzaSyAON6ej-MZMTh3xHP-uc_sBvZ0s5HXhRvM&channelId=UCpsmW5BWFjjecWw5lSv7GmQ&part=snippet,id&order=date&maxResults=10


import requests
video_list_request = requests.get('https://www.googleapis.com/youtube/v3/search?key=AIzaSyAON6ej-MZMTh3xHP-uc_sBvZ0s5HXhRvM&channelId=UCpsmW5BWFjjecWw5lSv7GmQ&part=snippet,id&order=date&maxResults=10')
video_list_json = video_list_request.json()
list_one = []
#video_list = video_list_json['items'][0]['snippet']['title']
for x in range(10):
    list_one.append(video_list_json['items'][x]['snippet']['title'])