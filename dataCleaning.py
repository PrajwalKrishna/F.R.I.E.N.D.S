import json
import os
import csv
users = []
for filename in os.listdir('./Features/'):
    with open('./Features/' + filename) as json_file:
        data = json.load(json_file)
        try:
            big5 = data['personality']
            user = { 'Name' : filename[:-5]}
            for i in big5:
                user[i['name']]=i['percentile']*100
            # needs = data['needs']
            # for need in needs:
            #     user[need['name']]=i['percentile']*100
            users.append(user)
        except:
            pass
print(len(users))
keys = users[0].keys()
with open('users.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(users)

records = []
# Making pairs
for user in users:
    username = user['Name']
    friends = []
    count = 25
    friends.append(username)
    if(os.path.isfile('./Friends/' + username + '.json')):
        with open('./Friends/' + username + '.json') as json_file:
            data = json.load(json_file)
            for friend in data:
                friends.append(friend)
    if(len(friends)<3):
        continue
    for id in users:
        record = {}
        for field in user:
            record['User ' + field] = user[field]
        for field in id:
            record['Friend ' + field] = id[field]
        if id['Name'] in friends:
            record['Friendship Status'] = 1
            records.append(record)
        else:
            record['Friendship Status'] = 0
            if(count):
                records.append(record)
                count -= 1
print(len(records))
keys = records[0].keys()
with open('records.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(records)
