import tweepy
import requests
import json
import os.path

consumer_key = 'Kt6WNY1DPSBLPkrFzQoE0TV6h'
consumer_secret = 'UUTUOUgIZ0uBijCWay4Y1j6Spb0JlYBFvngB4a1WeC1KK9kQmg'
access_token = '2951964404-Thlks6h0r7mboOf36Yk3dp1YCKgHYho0QdY7uCD'
access_token_secret = 'kBInoOMXY362LkAvRq87geWpqtdIxL93jOxviICVmFm1k'
ibmAuthoziation = 'mYMCHtOw3tfKY2ulgkbR2qv_Jc1UP26w3bN5Gf4zXxFP'
ibmBaseUrl = 'https://gateway-lon.watsonplatform.net/personality-insights/api'
ibmPersonalityUrl = ibmBaseUrl + '/v3/profile?version=2017-10-13'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# Calling api
api = tweepy.API(auth)

def get_tweets(username):
    if(os.path.isfile('./Dataset/' + username + '.txt')):
        return
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # # Calling api
    api = tweepy.API(auth)
    # 200 tweets to be extracted
    number_of_tweets=2000
    tweets = api.user_timeline(screen_name=username,count=number_of_tweets,tweet_mode="extended")

    f = open("./Dataset/" + username + ".txt", "w")
    for tweet in tweets:
        f.write(tweet.full_text + '\n')
    f.close()

def get_traits(username):
    if(os.path.isfile('./Features/' + username + '.json')):
        return
    path = "./Dataset/" + username + ".txt"
    data = open(path, 'rb').read()
    res = requests.post(
        ibmPersonalityUrl,
        auth=('apikey',ibmAuthoziation),
        headers={
            'Content-Type':'text/plain',
            'Accept':'application/json'
        },
        data = data
        )
    # print(res.text)

    response = res.json()
    # print(res.json())
    with open('./Features/' + username + '.json', 'w') as json_file:
        json.dump(response, json_file)
    # print(res)

def get_friends(username, depth=0):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # Calling api
    api = tweepy.API(auth)

    friends = api.friends_ids(screen_name=username)
    used_friends = set()
    if(len(friends)>10):
        friends = friends[2:10]
    for friend in friends:
        user = api.get_user(id=friend)
        print('cur ' + user.screen_name)
        get_tweets(user.screen_name)
        get_traits(user.screen_name)
        used_friends.add(user.screen_name)
        if(depth<2):
            get_friends(user.screen_name,depth+1)
    if(os.path.isfile('./Friends/' + username + '.json')):
        with open('./Friends/' + username + '.json') as json_file:
            data = json.load(json_file)
            for i in data:
                used_friends.add(i)
    print(list(used_friends))
    with open('./Friends/' + username + '.json', 'w') as json_file:
        json.dump(list(used_friends), json_file)

if __name__ == '__main__':
    get_friends("y5yash",1)
