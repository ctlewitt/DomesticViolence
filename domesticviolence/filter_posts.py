import json
import re
from domesticviolence.util import (get_tweet_parts, relevant_tweet, post_contains_commentary, post_contains_commentary2,
                                   post_contains_link, post_is_retweet, post_is_tweet, AUTHOR, CONTENT, MEDIA_PROVIDER)


DEBUG = False

# takes original file and filters into good file and bad file based on filter function
# filter function returns True if undesireable quality is present, False if it should not be filtered out (ie, good tweet)
def filter_out_by_func(original_file_name, good_file_name, bad_file_name, good_authors_file_name, filter_func):
    with open(original_file_name, "r") as original_f:
        with open(good_file_name, "w") as good_f:
            with open(bad_file_name, "w") as bad_f:
                #make set of user ids
                users = set()
                original_lines = 0
                good_lines = 0
                bad_lines = 0
                for line in original_f:
                    original_lines += 1
                    #split line on commas
                    tweet_parts = get_tweet_parts(line)
                    if DEBUG:
                        print ("TWEET_PARTS: ")
                        print (tweet_parts)
                    # sort line into good/bad file based on filter_func and update appropriate count
                    if (filter_func(tweet_parts)):
                        bad_f.write(line)
                        bad_lines += 1
                    else:
                        #add userid to the set
                        users.add(tweet_parts[AUTHOR].lower())
                        # add tweet to relevant tweets file
                        good_f.write(line)
                        good_lines += 1


            with open(good_authors_file_name, "w") as user_list_file:
                #turn set into list, dump list into string, write into file
                user_list_file.write(json.dumps(list(users)))
                num_relevant_authors = len(users)

    # print results
    print("total lines: {}\ngood lines: {} \nbad lines: {} \ngood authors: {}".format(original_lines, good_lines, bad_lines, num_relevant_authors))




# separates posts that are tweets from posts that are not tweets (has separate function because filter result is good
def filter_tweet_vs_post():
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

            with open("domesticviolence/hashtag_authors/WISWIL_twitter_users.txt", "w") as user_list_file:
                #turn set into list, dump list into string, write into file
                user_list_file.write(json.dumps(list(users)))
                num_relevant_authors = len(users)

    # print results
    print("total lines: {}\nfiltered lines: {} \nunfiltered lines: {} \nfiltered authors: {}".format(total_lines, filter_lines, non_filter_lines, num_relevant_authors))

def sequence_of_filters_applied():
    filter_tweet_vs_post() #splits into "hashtag_tweets/WISWIL_filtered_twitter_not.txt" and "hashtag_tweets/WISWIL_filtered_twitter.txt"
    filter_out_by_func("domesticviolence/hashtag_tweets/WISWIL_filtered_twitter.txt",
                       "domesticviolence/hashtag_tweets/WISWIL_filtered_noRTs.txt",
                       "domesticviolence/hashtag_tweets/WISWIL_filtered_hasRTs.txt",
                       "domesticviolence/hashtag_authors/WISWIL_twitter_users_noRTs.txt",
                       post_is_retweet)
    filter_out_by_func("domesticviolence/hashtag_tweets/WISWIL_filtered_noRTs.txt",
                       "domesticviolence/hashtag_tweets/WISWIL_filtered_nolinks.txt",
                       "domesticviolence/hashtag_tweets/WISWIL_filtered_haslinks.txt",
                       "domesticviolence/hashtag_authors/WISWIL_twitter_users_nolinks.txt",
                       post_contains_link)
    filter_out_by_func("domesticviolence/hashtag_tweets/WISWIL_filtered_nolinks.txt",
                       "domesticviolence/hashtag_tweets/WISWIL_filtered_nocommentary.txt",
                       "domesticviolence/hashtag_tweets/WISWIL_filtered_hascommentary.txt",
                       "domesticviolence/hashtag_authors/WISWIL_twitter_users_nocommentary.txt",
                       post_contains_commentary)

filter_out_by_func("domesticviolence/hashtag_tweets/WISWIL_filtered_nocommentary.txt",
                   "domesticviolence/hashtag_tweets/WISWIL_filtered_nocommentary2.txt",
                   "domesticviolence/hashtag_tweets/WISWIL_filtered_hascommentary2.txt",
                   "domesticviolence/hashtag_authors/WISWIL_twitter_users_nocommentary2.txt",
                   post_contains_commentary2)


# def unused_conglomerate_filter():
#     with open("hashtag_tweets/WhyIStayed_WhyILeft.csv", "r") as hashtag_file:
#         with open("hashtag_tweets/WISWIL_relevant_tweets.txt", "w") as relevant_tweets_file:
#             with open("hashtag_tweets/WISWIL_irrelevant_tweets.txt", "w") as irrelevant_tweets_file:
#                 #make set of user ids
#                 users = set()
#                 total_lines = 0
#                 relevant_lines = 0
#                 irrelevant_lines = 0
#                 for line in hashtag_file:
#                     total_lines += 1
#                     #split line on commas
#                     tweet_parts = get_tweet_parts(line)
#
#                     #if media source is TWITTER and content does not begin with "RT @":
#                     if (relevant_tweet(tweet_parts)):
#                         #add userid to the set
#                         users.add(tweet_parts[AUTHOR].lower())
#                         # add tweet to relevant tweets file
#                         relevant_tweets_file.write(line)
#                         relevant_lines += 1
#                     else:
#                         if (re.match(r'("?RT @)', tweet_parts[CONTENT]) is None and tweet_parts[MEDIA_PROVIDER] == "TWITTER"):
#                             irrelevant_tweets_file.write(tweet_parts[AUTHOR] + ", " + tweet_parts[CONTENT] + "\n")
#                             irrelevant_lines += 1
#
#
#             with open("list_of_old_WISWIL_filtered_users.txt", "w") as user_list_file:
#                 #turn set into list, dump list into string, write into file
#                 user_list_file.write(json.dumps(list(users)))
#                 num_relevant_authors = len(users)
#
#     # print results
#     print("total lines: {}\nrelevant lines: {} \nirrelevant lines: {} \nrelevant authors: {}".format(total_lines, relevant_lines, irrelevant_lines, num_relevant_authors))
#
