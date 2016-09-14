import json
import re
from domesticviolence.util import get_tweet_parts, relevant_tweet, AUTHOR, CONTENT, MEDIA_PROVIDER


if __name__ == "__main__":
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

