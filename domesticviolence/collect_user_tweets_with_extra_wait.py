import twitter
import sys
import json
import time
import os
from domesticviolence.util import connect_twitter_api

api = connect_twitter_api()

#get list of user accounts from list_of_users.txt
with open("list_of_old_WISWIL_users.txt", "r") as user_list_file:
    user_list = json.loads(user_list_file.readline())
#get all new tweets from each user in list
for user in user_list:
    #open user's file and set sincetweet based on it
    with open("tweets_by_users/" +user+".txt", "a+") as user_tweet_file:
        # set initial parameters for current user's tweet collection for the week
        sincetweet = 0
        maxtweet = sys.maxsize  # this will be maxsize at the beginning and update itself later
        tweet_count = 0
        user_tweet_file.seek(0)
        for line in user_tweet_file:
            tweet_count+=1
            sincetweet = max(sincetweet, int(json.loads(line)["id_str"]))
        #debugging
        print("user: " + user)
        print("tweets recorded: " + str(tweet_count))
        print("sincetweet: " + str(sincetweet))
        print("maxtweet: " + str(maxtweet))

        #TEMP ADDING TRY CATCH TO HANDLE RATE LIMITS
        results = api.GetSearch(term="from:"+user,
                            since_id=sincetweet,
                            max_id=maxtweet,
                            count=100,
                            result_type="recent")
        time.sleep(5.05)

        while len(results) > 0:
            for result in reversed(results):
                tweet_count+=1
                result_str = str(result)
                user_tweet_file.write(result_str + "\n")
                result_json = json.loads(result_str)
                maxtweet = min(maxtweet, int(result_json["id_str"]) - 1)
                #print (str(result))
                # debugging
                #print("setting sincetweet to: " + str(sincetweet) +"\n")
                # debugging
                #print("setting maxtweet to: " + str(maxtweet) +"\n")

            results = api.GetSearch(term="from:" + user,
                                    since_id=sincetweet,
                                    max_id=maxtweet,
                                    count=100,
                                    result_type="recent")
            time.sleep(5.05)

        # debugging
        print("sincetweet: " + str(sincetweet))
        print("maxtweet: " + str(maxtweet))
        print("new tweet count: " + str(tweet_count) + "\n")
