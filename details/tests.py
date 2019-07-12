from django.test import TestCase
from urllib.parse import urlparse

o = urlparse('https://www.facebook.com/permalink.php?story_fbid=2321006788227886&id=1740315322963705')

answer = o.query
final = answer.split('=')

print(final[2].split('&__')[0]+'_'+final[1].split('&id')[0])