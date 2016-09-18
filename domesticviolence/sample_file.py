from domesticviolence.util import (get_tweet_parts, MEDIA_PROVIDER, HEADLINE, AUTHOR, CONTENT, ARTICLE_URL, MEDIA_PROVIDER, PUBLISH_DATE,
                  FOLLOWING, FOLLOWERS, UPDATES, BLOG_POST_SENTIMENT, ARTICLE_ID)



'''line_num = 0
with open("WhyIStayed_WhyILeft.json", "r") as read_file:
    with open("miniWISWILjson.json", "w") as write_file:
        for line in read_file:
            line_num+=1
            if line_num >5000 and line_num <5500:
                write_file.write(line)
'''
"""
line_num = 0
with open("WhyIStayed_WhyILeft.csv", "r") as read_file:
    with open("miniWISWILjson.csv", "w") as write_file:
        while line_num < 500:
            line_num+=1
            line = read_file.readline()
            write_file.write(line)

"""
"""
line_num = 0
with open("WhyIStayed_WhyILeft.csv", "r") as read_file:
    while line_num < 500:
        line_num+=1
        print(read_file.readline())
"""
"""
line_num = 0
with open("WhyIStayed_WhyILeft.csv", "r") as read_file:
    for line in read_file:
        line_num += 1
print(line_num)
"""


# prints an evenly spaced sample of 100 lines from a document
def print_sample(filename, part=None):
    line_num = 0
    with open(filename, "r") as read_file:
        tweet_part_idxes = [HEADLINE, AUTHOR, CONTENT, ARTICLE_URL, MEDIA_PROVIDER, PUBLISH_DATE, FOLLOWING, FOLLOWERS,
                            UPDATES, BLOG_POST_SENTIMENT, ARTICLE_ID]
        words_for_tweet_parts = ["HEADLINE", "AUTHOR", "CONTENT", "ARTICLE_URL", "MEDIA_PROVIDER", "PUBLISH_DATE",
                                 "FOLLOWING", "FOLLOWERS", "UPDATES", "BLOG_POST_SENTIMENT", "ARTICLE_ID"]
        for line in read_file:
            line_num += 1
    print("Total lines in file: {}".format(line_num))
    with open(filename, "r") as read_file:
        frequency = line_num//100
        line_num = 0
        if part:
            tweet_part_idx = words_for_tweet_parts.index(part)
        for line in read_file:
            line_num += 1
            if line_num == frequency:
                tweet_parts = get_tweet_parts(line)
                if part:
                    print("{}: {}".format(part, tweet_parts[tweet_part_idx]))
                else:
                    for tweet_part_idx in tweet_part_idxes:
                        print("{}: {}".format(words_for_tweet_parts[tweet_part_idx], tweet_parts[tweet_part_idx]))
                line_num = 0
                print(line)

# function representing the calls made to print_sample to check contents of filtered files
def samples_done():
    print_sample("WISWIL_filtered_twitter.txt", "MEDIA_PROVIDER")
    print_sample("WISWIL_filtered_twitter_not.txt", "MEDIA_PROVIDER")
    print_sample("WISWIL_filtered_hasRTs.txt", "CONTENT")
    print_sample("WISWIL_filtered_noRTs.txt", "CONTENT")
    print_sample("WISWIL_filtered_haslinks.txt", "CONTENT")
    print_sample("WISWIL_filtered_nolinks.txt", "CONTENT")

