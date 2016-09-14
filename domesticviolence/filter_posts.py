import json
import re
from domesticviolence.util import (get_tweet_parts, relevant_tweet, post_contains_commentary, post_contains_link, post_is_retweet,
                  post_is_tweet, AUTHOR, CONTENT, MEDIA_PROVIDER)

def filter_twitter_content():
    with open("hashtag_tweets/WhyIStayed_WhyILeft.csv", "r") as hashtag_file:
        with open("hashtag_tweets/WISWIL_filtered_twitter.txt", "w") as twitter_tweets_file:
            with open("hashtag_tweets/WISWIL_filtered_twitter_not.txt", "w") as non_twitter_tweets_file:
                #make set of user ids
                users = set()
                total_lines = 0
                filter_lines = 0
                non_filter_lines = 0
                for line in hashtag_file:
                    total_lines += 1
                    #split line on commas
                    tweet_parts = get_tweet_parts(line)
                    print ("TWEET_PARTS: ")
                    print (tweet_parts)

                    # sort line into filtered or non-filter file and update appropriate count
                    if (post_is_tweet(tweet_parts)):
                        #add userid to the set
                        users.add(tweet_parts[AUTHOR].lower())
                        # add tweet to relevant tweets file
                        twitter_tweets_file.write(line)
                        filter_lines += 1
                    else:
                        non_twitter_tweets_file.write(line)
                        non_filter_lines += 1


            with open("WISWIL_twitter_users.txt", "w") as user_list_file:
                #turn set into list, dump list into string, write into file
                user_list_file.write(json.dumps(list(users)))
                num_relevant_authors = len(users)

    # print results
    print("total lines: {}\nfiltered lines: {} \nunfiltered lines: {} \nfiltered authors: {}".format(total_lines, filter_lines, non_filter_lines, num_relevant_authors))


filter_twitter_content()

def old_main():
    with open("hashtag_tweets/WhyIStayed_WhyILeft.csv", "r") as hashtag_file:
        with open("hashtag_tweets/WISWIL_relevant_tweets.txt", "w") as relevant_tweets_file:
            with open("hashtag_tweets/WISWIL_irrelevant_tweets.txt", "w") as irrelevant_tweets_file:
                #make set of user ids
                users = set()
                total_lines = 0
                relevant_lines = 0
                irrelevant_lines = 0
                for line in hashtag_file:
                    total_lines += 1
                    #split line on commas
                    tweet_parts = get_tweet_parts(line)

                    #if media source is TWITTER and content does not begin with "RT @":
                    if (relevant_tweet(tweet_parts)):
                        #add userid to the set
                        users.add(tweet_parts[AUTHOR].lower())
                        # add tweet to relevant tweets file
                        relevant_tweets_file.write(line)
                        relevant_lines += 1
                    else:
                        if (re.match(r'("?RT @)', tweet_parts[CONTENT]) is None and tweet_parts[MEDIA_PROVIDER] == "TWITTER"):
                            irrelevant_tweets_file.write(tweet_parts[AUTHOR] + ", " + tweet_parts[CONTENT] + "\n")
                            irrelevant_lines += 1


            with open("list_of_old_WISWIL_filtered_users.txt", "w") as user_list_file:
                #turn set into list, dump list into string, write into file
                user_list_file.write(json.dumps(list(users)))
                num_relevant_authors = len(users)

    # print results
    print("total lines: {}\nrelevant lines: {} \nirrelevant lines: {} \nrelevant authors: {}".format(total_lines, relevant_lines, irrelevant_lines, num_relevant_authors))

