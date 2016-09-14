import json

# compares the number of filtered vs unfiltered users

unfiltered_count = 0
filtered_count = 0
# with open("list_of_old_WISWIL_users.txt") as unfiltered_file:
#     unfiltered_list = json.loads(unfiltered_file.readline())
#     unfiltered_count += len(unfiltered_list)
with open("list_of_old_WISWIL_users_ALREADYDONE.txt") as unfiltered_file2:
    unfiltered_list = json.loads(unfiltered_file2.readline())
    unfiltered_count += len(unfiltered_list)
with open("list_of_old_WISWIL_filtered_users.txt") as filtered_file:
    filtered_list = json.loads(filtered_file.readline())
    filtered_count += len(filtered_list)
print("unfiltered count: " + str(unfiltered_count))
print("filtered count: " + str(filtered_count))
