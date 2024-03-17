import json
from os import listdir


"""user_file = []
for file in listdir("data/selected_files_4_annotation"):
    with open(f"data/selected_files_4_annotation/{file}", "r") as f:
        user_file.append(json.load(f))


with open("data/user1.json", "w") as f:
    f.write(json.dumps(user_file, indent=4))"""

user_file = []
count = 0
for file in listdir("data/selected_files_4_annotation"):
    if file.endswith(".json"):
        with open(f"data/selected_files_4_annotation/{file}", "r") as f:
            this_page = json.load(f)
            # user_file.append(json.load(f))
        this_page['checkboxes'] = [True for _ in this_page['event_list']]
        user_file.append(this_page)
        if len(user_file) >= 5:
            with open(f"data/group_{count}.json", "w") as f:
                f.write(json.dumps(user_file, indent=4))
            count += 1
            user_file = []