"""
Reads JSON from Instagram followers and returns who is not following you back

**Guide**

Go to https://accountscenter.instagram.com/info_and_permissions/dyi/
Request followers data
Run script (consider the folder below)

"""
import json

HOME = '/Users/arturmagalhaes/Downloads/connections/followers_and_following'

with open(f'{HOME}/following.json', 'r') as file:
    following = json.load(file)

with open(f'{HOME}/followers_1.json', 'r') as file:
    followers = json.load(file)

following = following['relationships_following']

followers_set = set()
following_set = set()

for follow in following:
    following_set.add(follow['string_list_data'][0]['value'])

for follower in followers:
    followers_set.add(follower['string_list_data'][0]['value'])


not_following_back = list()
for follow in following_set:
    if follow not in followers_set:
        not_following_back.append(follow)

with open('not_following_back.txt', 'w') as f:
    for item in not_following_back:
        f.write(f"{item}\n")
