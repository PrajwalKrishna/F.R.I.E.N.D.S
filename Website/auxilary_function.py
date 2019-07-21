import tweepy
import requests
import json
import os.path
import numpy as np
import pandas as pd
import pickle

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
    os.remove('./Dataset/' + username + '.txt')
    return res.json()

def cleanData(jsonResponse,user):
    try:
        big5 = jsonResponse['personality']
        user = { 'Name' : user}
        for i in big5:
            user[i['name']]=i['percentile']*100
        return user
    except:
        return False

def run_logistic_regression(data):
    with open('../logisticRegression.pkl', 'rb') as f:
        logreg = pickle.load(f)
    train = pd.read_csv("./users.csv")
    train.sample(frac=1)
    X = train.drop(columns=["Name"],axis=1)
    name_array = list(train["Name"])
    X['User Openness'] = data['Openness']
    X['User Conscientiousness'] = data['Conscientiousness']
    X['User Extraversion'] = data['Extraversion']
    X['User Agreeableness'] = data['Agreeableness']
    X['User Emotional range'] = data['Emotional range']
    X = X.rename(columns={
        'Openness':'Friend Openness',
        'Conscientiousness':'Friend Conscientiousness',
        'Extraversion':'Friend Extraversion',
        'Agreeableness':'Friend Agreeableness',
        'Emotional range':'Friend Emotional range'
        })
    X = X[['User Openness','User Conscientiousness','User Extraversion','User Agreeableness','User Emotional range',
        'Friend Openness','Friend Conscientiousness','Friend Extraversion','Friend Agreeableness','Friend Emotional range']]
    H = logreg.decision_function(X)
    arr = np.array(H)
    a = arr.argsort()[-10:][::-1]
    ans = []
    for i in a:
        ans.append(name_array[i])
    return ans

def utilityFunction(user):
    get_tweets(user)
    personality = get_traits(user)
    data = cleanData(personality,user)
    if(data):
        return run_logistic_regression(data)
